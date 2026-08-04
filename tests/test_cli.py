import subprocess, sys, pathlib, json
root=pathlib.Path(__file__).resolve().parents[1]
out=subprocess.check_output([sys.executable,str(root/'src'/'video_caption_safe_area_checker.py'),str(root/'examples'/'captions.json'),'--json'], text=True)
data=json.loads(out); assert data['unsafe_count']==1
print('ok video-caption-safe-area-checker')
