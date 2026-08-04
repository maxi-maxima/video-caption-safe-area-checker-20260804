#!/usr/bin/env python
import argparse, json
PRESETS={'vertical-short':{'w':1080,'h':1920,'unsafe':{'top':160,'bottom':300,'left':70,'right':70}},'landscape-video':{'w':1920,'h':1080,'unsafe':{'top':80,'bottom':120,'left':40,'right':40}}}
def check(captions,preset):
 p=PRESETS[preset]; u=p['unsafe']; safe=(u['left'],u['top'],p['w']-u['right'],p['h']-u['bottom'])
 res=[]
 for c in captions:
  x,y,w,h=[int(c[k]) for k in ['x','y','w','h']]; box=(x,y,x+w,y+h)
  ok=box[0]>=safe[0] and box[1]>=safe[1] and box[2]<=safe[2] and box[3]<=safe[3]
  res.append({'text':c.get('text',''), 'box':box, 'safe':ok, 'safe_area':safe, 'problem': '' if ok else 'caption overlaps platform UI unsafe area'})
 return res

def main():
 p=argparse.ArgumentParser(description='Check burned-in video captions against platform safe areas.')
 p.add_argument('captions_json'); p.add_argument('--preset',choices=PRESETS,default='vertical-short'); p.add_argument('--json',action='store_true')
 a=p.parse_args(); caps=json.load(open(a.captions_json,encoding='utf-8')); res=check(caps,a.preset)
 if a.json: print(json.dumps({'preset':a.preset,'results':res,'unsafe_count':sum(not r['safe'] for r in res)},indent=2,ensure_ascii=False))
 else:
  for r in res: print(('OK  ' if r['safe'] else 'BAD ')+r['text']+' '+str(r['box'])+' '+r['problem'])
if __name__=='__main__': main()
