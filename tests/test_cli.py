import json
import pathlib
import subprocess
import sys

root = pathlib.Path(__file__).resolve().parents[1]
cli = [sys.executable, str(root / 'src' / 'video_caption_safe_area_checker.py')]

out = subprocess.check_output(cli + [str(root / 'examples' / 'captions.json'), '--json'], text=True)
data = json.loads(out)
assert data['unsafe_count'] == 1
unsafe = [r for r in data['results'] if not r['safe']][0]
assert unsafe['unsafe_overlap_ratio'] > 0
assert unsafe['edge_offsets']['bottom'] < 0

custom = subprocess.check_output(
    cli + [str(root / 'examples' / 'captions.json'), '--frame', '1080x1920', '--unsafe', '100,50,50,50', '--json'],
    text=True,
)
custom_data = json.loads(custom)
assert custom_data['unsafe_count'] == 0
assert all(r['unsafe_overlap_ratio'] == 0 for r in custom_data['results'])

markdown = subprocess.check_output(cli + [str(root / 'examples' / 'captions.json'), '--format', 'markdown'], text=True)
assert '# Caption safe-area report' in markdown
assert '| ⚠️ Unsafe |' in markdown
assert 'Unsafe overlap' in markdown

bad = subprocess.run(
    cli + [str(root / 'examples' / 'captions.json'), '--frame', '100x100', '--unsafe', '60,60,0,0'],
    text=True,
    capture_output=True,
)
assert bad.returncode == 2 and 'leave no safe area' in bad.stderr
print('ok video-caption-safe-area-checker')
