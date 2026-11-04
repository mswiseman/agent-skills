---
name: segmentation-annotation-tool
description: Build a local browser-based image segmentation annotation editor from images alone or images with existing masks, with brush, eraser, Bezier pen, magic wand, binary-mask view, undo, and review/export controls.
---

# Segmentation annotation tool

Create a working annotation editor using the bundled template and builder. It operates locally, preserves original image dimensions, supports overlapping per-class masks, and needs no labeling service or training model. Do not generate biological ground truth or mark proposals reviewed automatically.

## Inputs and build

Accept a directory of images, or a JSON manifest with associated segmentation masks. Read [references.md](references.md) for the manifest and export schemas, supported formats, and practical limits. Preserve image identity, class names, review state, and any train/validation/test partition metadata. Use generic class `foreground` for images alone unless classes are provided. Do not inherit trichome class names, 224×224 dimensions, or old project paths.

Run `python scripts/build_editor.py --images /absolute/images --output /absolute/output/review.html` for images alone. Add `--classes class_a,class_b` when known. For masks, use `--manifest /absolute/manifest.json --output /absolute/output/review.html`. The builder requires Pillow and rejects ambiguous or mismatched input instead of resizing masks silently. Use an available Python environment with Pillow, or install it only when needed.

The generated HTML embeds its data and works offline. It includes brush and eraser with pixel diameter, connected-color magic wand with tolerance and add/erase action, a click/drag Bezier pen with fill/cancel, overlay opacity, binary view, per-class controls, undo/redo (Ctrl/Cmd+Z, Ctrl/Cmd+Shift+Z), review status, image navigation, local autosave, and JSON/PNG export and restore. A committed edit clears the image's reviewed flag. Pen paths are draft geometry until filled; navigation/tool changes cancel unfinished paths. Undo first removes draft pen anchors, then reverses committed mask edits. Brush output and pen fills are thresholded to exact binary pixels.

If another annotation format is supplied (COCO polygons/RLE, Labelbox export, indexed multiclass PNG, etc.), convert it into native-resolution binary PNGs per class and the manifest before building; the builder does not claim to import these formats directly. Preserve holes and overlaps. Reject unresolved class mapping or coordinate/image mismatches. Keep originals intact. Mask value 0 is background and nonzero is foreground only when an explicit threshold/foreground rule is given; the builder itself accepts exact 0/255 binary masks.

## Delivery and verification

Deliver the generated HTML and explain how to open it, export all work, and reopen/restore the JSON. All images are included in JSON export, with reviewed flags; users must explicitly filter reviewed images for training. The downloaded current-class PNG has native dimensions and exact 0/255 foreground. JSON stores all per-class PNGs, including blank masks. Local browser storage is a convenience, not a durable backup; quota failures are surfaced in the editor. Large collections should be split into manageable batches; do not downsample images to fit memory without the user's agreement.

Run `scripts/smoke_test.py` to check builder invariants and HTML embedding. For frontend changes, also exercise the generated page in an available browser using that environment's browser skill, including brush/erase, pen fill, wand tolerance, undo/redo shortcuts, navigation, review invalidation, and JSON restore. Check a non-square image and exported PNG dimensions/pixel values. Report which checks actually ran. Validate the skill with the skill-creator validator when available.
