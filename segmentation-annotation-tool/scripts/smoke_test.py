#!/usr/bin/env python3
import json,tempfile,re
from pathlib import Path
from PIL import Image
from build_editor import build
with tempfile.TemporaryDirectory() as tmp:
 r=Path(tmp);(r/'images').mkdir();Image.new('RGB',(96,48),'green').save(r/'images/a.png');Image.new('RGB',(48,96),'gray').save(r/'images/b.png')
 p=build(images=r/'images',output=r/'blank.html');html=p.read_text();assert '"width": 96, "height": 48' in html and '__DATA__' not in html
 Image.new('L',(96,48),255).save(r/'mask.png');spec={'classes':['one','two'],'images':[{'id':'</script><script>bad()</script>','image':'images/a.png','masks':{'one':'mask.png'}}]};(r/'manifest.json').write_text(json.dumps(spec));p=build(manifest=r/'manifest.json',output=r/'with_masks.html');assert '</script><script>bad()' not in p.read_text()
 for bad in [Image.new('L',(95,48),255),Image.new('L',(96,48),127)]:
  bad.save(r/'mask.png')
  try:build(manifest=r/'manifest.json',output=r/'bad.html')
  except ValueError:pass
  else:raise AssertionError('Invalid mask was accepted')
 print('PASS: images-only, non-square sizes, multiclass/blank masks, safe embedding, bad dimensions and nonbinary rejection')
