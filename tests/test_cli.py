import subprocess, sys, pathlib, json
root=pathlib.Path(__file__).resolve().parents[1]
out=subprocess.check_output([sys.executable,str(root/'src'/'video_caption_safe_area_checker.py'),str(root/'examples'/'captions.json'),'--json'], text=True)
data=json.loads(out); assert data['unsafe_count']==1
custom=subprocess.check_output([sys.executable,str(root/'src'/'video_caption_safe_area_checker.py'),str(root/'examples'/'captions.json'),'--frame','1080x1920','--unsafe','100,50,50,50','--json'], text=True)
custom_data=json.loads(custom); assert custom_data['unsafe_count']==0
bad=subprocess.run([sys.executable,str(root/'src'/'video_caption_safe_area_checker.py'),str(root/'examples'/'captions.json'),'--frame','100x100','--unsafe','60,60,0,0'], text=True, capture_output=True)
assert bad.returncode==2 and 'leave no safe area' in bad.stderr
print('ok video-caption-safe-area-checker')
