#!/usr/bin/env python3
"""Build a self-contained, native-resolution segmentation editor. Requires Pillow."""
import argparse, base64, hashlib, io, json
from pathlib import Path
from PIL import Image
EXT={'.png','.jpg','.jpeg','.tif','.tiff','.bmp','.webp'}
def png(im):
 b=io.BytesIO();im.save(b,format='PNG');return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
def build(images=None,manifest=None,classes=None,output=None):
 if manifest:
  path=Path(manifest).resolve();spec=json.loads(path.read_text());root=path.parent
 else:
  root=Path(images).resolve();spec={'classes':classes or ['foreground'],'images':[{'id':p.relative_to(root).as_posix(),'image':str(p)} for p in sorted(root.rglob('*')) if p.suffix.lower() in EXT]}
 names=spec.get('classes');records=spec.get('images',[])
 if not isinstance(names,list) or not names or any(not isinstance(c,str) or not c.strip() for c in names) or len(set(names))!=len(names):raise ValueError('Classes must be distinct nonempty strings')
 if not records:raise ValueError('No images supplied')
 data=[];seen=set()
 for r in records:
  ident=r['id']
  if not isinstance(ident,str) or not ident or ident in seen:raise ValueError('Image IDs must be distinct nonempty strings')
  seen.add(ident);path=(root/r['image']).resolve();raw=path.read_bytes()
  with Image.open(path) as source:
   if source.getexif().get(274,1)!=1:raise ValueError('Normalize image EXIF orientation together with masks first: '+ident)
   source=source.convert('RGB');w,h=source.size;source_url=png(source)
  masks={};given=r.get('masks',{})
  if set(given)-set(names):raise ValueError('Unknown mask class: '+ident)
  for name in names:
   if name in given:
    with Image.open(root/given[name]) as m:
     if m.size!=(w,h):raise ValueError('Mask size mismatch: '+ident)
     rgba=m.convert('RGBA');channels=rgba.split()
     if channels[3].getextrema()!=(255,255) or channels[0].tobytes()!=channels[1].tobytes() or channels[0].tobytes()!=channels[2].tobytes():raise ValueError('Mask must be opaque grayscale binary: '+ident)
     binary=channels[0]
     if sum(binary.histogram()[1:255]):raise ValueError('Mask values must be 0 or 255: '+ident)
     masks[name]=png(binary)
   else:masks[name]=png(Image.new('L',(w,h),0))
  data.append({'id':ident,'source_sha256':hashlib.sha256(raw).hexdigest(),'width':w,'height':h,'source':source_url,'masks':masks,'reviewed':r.get('reviewed') is True,'metadata':r.get('metadata',{})})
 identity=hashlib.sha256(json.dumps({'classes':names,'images':[(r['id'],r['source_sha256']) for r in data]},sort_keys=True).encode()).hexdigest()
 payload={'schema':'segmentation-editor-v1','dataset_id':identity,'title':spec.get('title','Segmentation annotation editor'),'classes':names,'images':data}
 template=(Path(__file__).resolve().parents[1]/'assets/editor.html').read_text()
 # Escape HTML script boundaries even in user-controlled IDs and metadata.
 encoded=json.dumps(payload,ensure_ascii=True).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
 target=Path(output).resolve();target.parent.mkdir(parents=True,exist_ok=True);target.write_text(template.replace('__DATA__',encoded));return target
if __name__=='__main__':
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--images');g.add_argument('--manifest');p.add_argument('--classes');p.add_argument('--output',required=True);a=p.parse_args();print(build(a.images,a.manifest,a.classes.split(',') if a.classes else None,a.output))
