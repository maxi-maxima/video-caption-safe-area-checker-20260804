# video-caption-safe-area-checker-20260804

## 解决的痛点

技术短视频字幕经常被平台 UI 遮挡，影响理解和完播。

## 为什么现在值得做

Developer content and AI-generated multimedia are growing; a no-dependency CLI that checks caption bounding boxes is quick to adopt in content pipelines.

## 安装与运行

无需第三方依赖，使用 Python 3.10+。

```bash
python src/video_caption_safe_area_checker.py --help
python src/video_caption_safe_area_checker.py examples/captions.json
python tests/test_cli.py
```

## 示例

示例输入位于 `examples/`，可运行：

```bash
python src/video_caption_safe_area_checker.py examples/captions.json
```

## 路线图

- SRT/VTT parser
- PNG visual overlay export
- Custom platform presets

## 许可证

MIT
