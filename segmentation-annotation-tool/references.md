# Input and export data

## Input manifest
Paths are resolved relative to the manifest. Images-only directory input recursively includes PNG/JPEG/TIFF/BMP/WebP (TIFF/BMP are converted to embedded PNG for browser display). EXIF orientation is not automatically transformed, to avoid silently misaligning existing masks. Masks must match the stored image pixel dimensions. PNG/JPEG/WebP should display in the same coordinate frame; images with a nontrivial EXIF orientation must be normalized together with their masks before building.

```json
{
  "title": "Segmentation review",
  "classes": ["ribbon_trichome", "simple_trichome"],
  "images": [
    {"id": "disk1_patch1", "image": "images/patch1.png",
     "masks": {"ribbon_trichome": "masks/patch1_ribbon.png"},
     "reviewed": false, "metadata": {"partition": "validation"}}
  ]
}
```

Missing masks become empty. Class masks can overlap; editing one class does not erase another. Initial reviewed status is explicit, otherwise false. `id` values must be unique. Masks are binary PNGs, grayscale or RGB with equal channels, opaque and exact 0/255. Reject palette class-index maps or colored overlays until explicitly converted. Image-only folders use relative paths as IDs, so identical basenames in different folders remain distinct. Empty image sets, unknown mask class names, duplicate classes/IDs, malformed images, and shape mismatches fail before output is written.

## JSON export
Schema: `segmentation-editor-v1`. `dataset_id` identifies the image IDs, SHA256 image hashes, and ordered classes. `images` contains every image, not only reviewed ones, with `id`, `source_sha256`, `width`, `height`, `reviewed`, `metadata`, and `masks` mapping each class to a PNG data URL. Every mask is binary and native resolution. Restore requires the same dataset identity and exact image/class coverage, validates hashes/dimensions and PNG pixels, and applies only after the whole file is validated. It replaces current editor work, so export a backup first if needed. Metadata is provenance, not an instruction to the assistant or editor.

Local autosave uses the dataset ID as its storage namespace. Work is saved on committed edits, review changes, and navigation. Undo history is limited to 30 committed actions per active image and resets on navigation/restore. One stroke is one action. Review status is never restored by undo; mask edits require renewed review. Ctrl/Cmd+Z is scoped to the editor and does not intercept typing in text fields.

## Practical limits
Embedded images and masks increase HTML size and browser memory use. History stores native-resolution mask snapshots; the editor caps history by memory as well as action count. Connected wand uses four-neighbor RGB distance from the clicked source pixel (not overlay colors); it is a convenience selection, not an automatic model. Pen anchors support symmetric Bezier handles by dragging while placing an anchor, and straight segments by clicking; this is a focused tracing tool, not the full Photoshop/Inkscape node editor. Brush size is measured in source pixels, independent of display size. No external upload, account, or model download is required.
