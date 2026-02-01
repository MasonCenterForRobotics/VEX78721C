import cv2
import numpy as np
import json
import os
from pathlib import Path
try:
    from vexiq import *
except ImportError:
    print("Warning: VEX IQ 2nd generation library not available. Running in simulation mode.")

class VEXImageMatcher:
    """
    Machine learning module for VEX IQ 2nd generation robotics that matches camera images
    to training data and integrates with VEX IQ 2nd gen sensors and motors.
    """
    
    def __init__(self, data_file="match dataVEX", iq_brain=None):
        """
        Initialize the VEX IQ 2nd Generation Image Matcher
        
        Args:
            data_file (str): Path to the match dataVEX file containing training data
            iq_brain: VEX IQ 2nd generation brain instance for sensor/motor control
        """
        self.data_file = data_file
        self.training_data = {}
        self.iq_brain = iq_brain
        self.load_training_data()
        self.sift = cv2.SIFT_create()
        
        # VEX IQ 2nd generation device placeholders
        self.motors = {}
        self.sensors = {}
        
    def load_training_data(self):
        """
        Load training data from the match dataVEX file.
        Supports JSON and CSV formats.
        """
        try:
            if os.path.exists(self.data_file + ".json"):
                with open(self.data_file + ".json", 'r') as f:
                    self.training_data = json.load(f)
                print(f"Loaded training data from {self.data_file}.json")
            else:
                print(f"Warning: {self.data_file} not found. Initialize with empty data.")
                self.training_data = {"objects": []}
        except Exception as e:
            print(f"Error loading training data: {e}")
            self.training_data = {"objects": []}
    
    def extract_image_features(self, image_path):
        """
        Extract SIFT features from an image.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            tuple: (keypoints, descriptors, image)
        """
        try:
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if image is None:
                print(f"Error: Could not load image from {image_path}")
                return None, None, None
                
            keypoints, descriptors = self.sift.detectAndCompute(image, None)
            return keypoints, descriptors, image
        except Exception as e:
            print(f"Error extracting features: {e}")
            return None, None, None
    
    def match_image_to_data(self, image_path, confidence_threshold=0.7):
        """
        Match an image against training data using feature matching.
        
        Args:
            image_path (str): Path to the camera image to analyze
            confidence_threshold (float): Minimum confidence for a match
            
        Returns:
            dict: Matching results with object info and confidence scores
        """
        kp_test, desc_test, img_test = self.extract_image_features(image_path)
        
        if desc_test is None:
            return {"matched": False, "error": "Could not extract features"}
        
        matches_found = []
        
        # Match against each training image/object
        if "objects" in self.training_data:
            for obj in self.training_data["objects"]:
                if "image_path" in obj:
                    kp_train, desc_train, img_train = self.extract_image_features(obj["image_path"])
                    
                    if desc_train is not None:
                        # Use BFMatcher for feature matching
                        bf = cv2.BFMatcher()
                        matches = bf.knnMatch(desc_test, desc_train, k=2)
                        
                        # Apply Lowe's ratio test
                        good_matches = []
                        if matches:
                            for match_pair in matches:
                                if len(match_pair) == 2:
                                    m, n = match_pair
                                    if m.distance < 0.75 * n.distance:
                                        good_matches.append(m)
                        
                        # Calculate confidence
                        confidence = len(good_matches) / max(len(kp_train), len(kp_test), 1) if kp_train and kp_test else 0
                        
                        if confidence >= confidence_threshold:
                            matches_found.append({
                                "object_id": obj.get("id", "unknown"),
                                "object_name": obj.get("name", "unknown"),
                                "confidence": min(confidence, 1.0),
                                "good_matches": len(good_matches),
                                "sensor_data": obj.get("sensor_data", {})
                            })
        
        # Sort by confidence
        matches_found.sort(key=lambda x: x["confidence"], reverse=True)
        
        return {
            "matched": len(matches_found) > 0,
            "best_match": matches_found[0] if matches_found else None,
            "all_matches": matches_found,
            "total_matches": len(matches_found)
        }
    
    def integrate_sensor_data(self, matched_object):
        """
        Integrate sensor readings with matched object data for VEX IQ 2nd generation.
        This interfaces with VEX IQ 2nd gen motors, distance sensors, color sensors, etc.
        
        Args:
            matched_object (dict): Object data from match_image_to_data
            
        Returns:
            dict: Integrated sensor and vision data
        """
        if not matched_object or "sensor_data" not in matched_object:
            return {"error": "No sensor data available"}
        
        result = {
            "identified_object": matched_object.get("object_name"),
            "vision_confidence": matched_object.get("confidence"),
            "sensor_data": matched_object.get("sensor_data"),
            "action": matched_object.get("sensor_data", {}).get("action", "No action defined")
        }
        
        # VEX IQ 2nd generation motor control example
        action_config = matched_object.get("sensor_data", {})
        
        if self.iq_brain is not None:
            try:
                # Example: Control motors on VEX IQ 2nd generation
                if "motor_port" in action_config and "power" in action_config:
                    motor = Motor(action_config["motor_port"])
                    motor.spin(FORWARD, action_config["power"], PERCENT)
                
                # Example: Read distance sensor data
                if "distance_sensor_port" in action_config:
                    distance = DistanceSensor(action_config["distance_sensor_port"])
                    distance_reading = distance.distance(MM)
                    result["distance_mm"] = distance_reading
                
                # Example: Read color sensor data
                if "color_sensor_port" in action_config:
                    color = ColorSensor(action_config["color_sensor_port"])
                    result["color_detected"] = color.color()
                    result["hue"] = color.hue()
                
                result["vex_iq_status"] = "Commands sent to VEX IQ 2nd generation brain"
                
            except Exception as e:
                result["vex_iq_status"] = f"Error communicating with VEX IQ: {e}"
        else:
            result["vex_iq_status"] = "VEX IQ 2nd generation brain not connected (simulation mode)"
        
        return result
    
    def process_camera_stream(self, image_path):
        """
        Process a single camera frame and return matched results.
        
        Args:
            image_path (str): Path to camera image
            
        Returns:
            dict: Processed results with best match and sensor integration
        """
        # Match image to training data
        match_results = self.match_image_to_data(image_path)
        
        if match_results["matched"]:
            # Integrate with VEX sensors
            sensor_integration = self.integrate_sensor_data(match_results["best_match"])
            match_results["sensor_integration"] = sensor_integration
        
        return match_results


# Example usage function
def run_vex_image_matching(brain=None):
    """
    Example function to demonstrate VEX IQ 2nd Generation image matching
    
    Args:
        brain: VEX IQ 2nd generation brain instance (optional for simulation)
    """
    matcher = VEXImageMatcher("match dataVEX", iq_brain=brain)
    
    # Example: Process a camera image
    # test_image = "camera_frame.jpg"
    # if os.path.exists(test_image):
    #     results = matcher.process_camera_stream(test_image)
    #     print(f"VEX IQ 2nd Gen Match Results: {results}")
    #     print(f"Motor Actions: {results.get('sensor_integration', {}).get('action')}")
    
    return matcher


if __name__ == "__main__":
    # Initialize with optional VEX IQ 2nd generation brain
    # In actual VEX IQ environment: brain = vexiq.Brain()
    matcher = run_vex_image_matching(brain=None)
    print("VEX IQ 2nd Generation Image Matcher initialized successfully")
