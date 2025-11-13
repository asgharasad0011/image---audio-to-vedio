#!/usr/bin/env python3
"""
MuseTalk - Simple Image Speech Generator
Usage: python run.py --image photo.jpg --audio speech.wav
"""

import os
import sys
import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser(description="MuseTalk - Make image speak")
    parser.add_argument("--image", type=str, required=True, help="Input image path")
    parser.add_argument("--audio", type=str, required=True, help="Input audio path")
    parser.add_argument("--output", type=str, default="output.mp4", help="Output video path")
    
    args = parser.parse_args()
    
    # Validate inputs
    if not os.path.exists(args.image):
        print(f"ERROR: Image not found: {args.image}")
        sys.exit(1)
    
    if not os.path.exists(args.audio):
        print(f"ERROR: Audio not found: {args.audio}")
        sys.exit(1)
    
    print(f"Image: {args.image}")
    print(f"Audio: {args.audio}")
    print(f"Output: {args.output}")
    print("\nProcessing with MuseTalk model...")
    
    # Get paths
    musetalk_dir = os.path.join(os.path.dirname(__file__), "MuseTalk")
    
    if not os.path.exists(musetalk_dir):
        print(f"ERROR: MuseTalk directory not found at {musetalk_dir}")
        sys.exit(1)
    
    # Get absolute paths
    image_path = os.path.abspath(args.image)
    audio_path = os.path.abspath(args.audio)
    
    # Create temp config file
    config_content = f"""task_0:
 video_path: "{image_path}"
 audio_path: "{audio_path}"
"""
    
    config_file = os.path.join(musetalk_dir, "configs/inference", "temp_test.yaml")
    with open(config_file, "w") as f:
        f.write(config_content)
    
    # Run MuseTalk inference from MuseTalk directory
    original_dir = os.getcwd()
    os.chdir(musetalk_dir)
    
    cmd = [
        sys.executable, "-m", "scripts.inference",
        "--inference_config", "configs/inference/temp_test.yaml",
        "--result_dir", "results",
        "--unet_model_path", "models/musetalkV15/unet.pth",
        "--unet_config", "models/musetalkV15/musetalk.json",
        "--version", "v15",
    ]
    
    try:
        os.makedirs("results", exist_ok=True)
        print("Running MuseTalk inference...")
        
        result = subprocess.run(cmd, check=False)
        
        os.chdir(original_dir)
        
        if result.returncode == 0:
            print(f"\n✓ Done! Output video in: {musetalk_dir}/results/")
        else:
            print(f"\nERROR: Inference failed")
            sys.exit(1)
        
    except Exception as e:
        os.chdir(original_dir)
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
