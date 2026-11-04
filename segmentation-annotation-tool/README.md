# Segmentation Annotation Tool

Create an offline browser editor from images alone or images with existing segmentation masks. It includes a brush, eraser, adjustable brush size, Bézier pen, magic wand, binary-mask view, undo/redo, review flags, and JSON/PNG export.

## Install in Codex

Unzip `segmentation-annotation-tool.zip` and place the extracted folder here:

```text
~/.codex/skills/segmentation-annotation-tool/
```

Start a new Codex chat and ask:

> Use $segmentation-annotation-tool to create an annotation editor for the images in `/path/to/images`, with classes `ribbon_trichome` and `simple_trichome`.

## Install in Claude Code

Unzip the same ZIP and place the extracted folder here:

```text
~/.claude/skills/segmentation-annotation-tool/
```

Start a new Claude Code session and ask:

> Use the segmentation-annotation-tool skill to create an annotation editor for the images in `/path/to/images`, with classes `ribbon_trichome` and `simple_trichome`.

The folder should contain `SKILL.md`, `scripts/`, and `assets/`. Claude can ignore the Codex-specific `agents/openai.yaml` file.

## Provide images and optional masks

Give the assistant the image folder and desired class names. If you already have annotations, also provide their location and format, and explain how they match the images. The skill supports native-resolution binary masks per class; other annotation formats need conversion first.

The builder requires Python and Pillow. The assistant can help set these up.

## Share with annotators

Send the generated `review.html` directly to an annotator. It contains the images and starting masks and opens in a browser without Codex, Claude, or an account.

- Choose an image and class, then edit its mask.
- Use Ctrl/Cmd+Z to undo and Ctrl/Cmd+Shift+Z to redo when focus is outside an input field.
- Mark an image reviewed only after checking all its masks. Further edits clear that flag.
- Export **all edits JSON** regularly and return that file to the project owner. It includes reviewed and unreviewed images and can be restored into the matching editor.
- Download the active-class PNG when an individual binary mask is needed.

Browser autosave is a convenience, not a durable backup. Keep exported JSON files. Only explicitly reviewed images should be selected for training.
