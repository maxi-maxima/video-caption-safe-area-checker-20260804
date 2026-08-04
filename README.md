# video-caption-safe-area-checker-20260804

Creators generating technical clips often burn captions into areas hidden by Shorts/TikTok/Reels UI chrome, hurting comprehension and retention.

## Why now

Developer content and AI-generated multimedia are growing; a no-dependency CLI that checks caption bounding boxes is quick to adopt in content pipelines.

## Install and run

No third-party dependencies are required. Use Python 3.10+.

```bash
python src/video_caption_safe_area_checker.py --help
python src/video_caption_safe_area_checker.py examples/captions.json
python tests/test_cli.py
```

## Example

Sample input lives in `examples/`. Example command:

```bash
python src/video_caption_safe_area_checker.py examples/captions.json
```

## Roadmap

- SRT/VTT parser
- PNG visual overlay export
- Custom platform presets

## License

MIT
