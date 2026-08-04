#!/usr/bin/env python
import argparse, json
PRESETS={'vertical-short':{'w':1080,'h':1920,'unsafe':{'top':160,'bottom':300,'left':70,'right':70}},'landscape-video':{'w':1920,'h':1080,'unsafe':{'top':80,'bottom':120,'left':40,'right':40}}}
def parse_frame(value):
 try: w,h=[int(x) for x in value.lower().split('x',1)]
 except ValueError: raise argparse.ArgumentTypeError('use WIDTHxHEIGHT, e.g. 1080x1920')
 if w<=0 or h<=0: raise argparse.ArgumentTypeError('frame dimensions must be positive')
 return w,h

def parse_unsafe(value):
 try: top,bottom,left,right=[int(x) for x in value.split(',')]
 except ValueError: raise argparse.ArgumentTypeError('use TOP,BOTTOM,LEFT,RIGHT, e.g. 160,300,70,70')
 if min(top,bottom,left,right)<0: raise argparse.ArgumentTypeError('unsafe margins cannot be negative')
 return {'top':top,'bottom':bottom,'left':left,'right':right}

def safe_area(preset, frame=None, unsafe=None):
 p=PRESETS[preset]; w,h=frame or (p['w'],p['h']); u=unsafe or p['unsafe']
 if u['left']+u['right']>=w or u['top']+u['bottom']>=h: raise ValueError('unsafe margins leave no safe area')
 return (u['left'],u['top'],w-u['right'],h-u['bottom'])

def check(captions,preset,frame=None,unsafe=None):
 safe=safe_area(preset,frame,unsafe)
 res=[]
 for c in captions:
  x,y,w,h=[int(c[k]) for k in ['x','y','w','h']]; box=(x,y,x+w,y+h)
  ok=box[0]>=safe[0] and box[1]>=safe[1] and box[2]<=safe[2] and box[3]<=safe[3]
  res.append({'text':c.get('text',''), 'box':box, 'safe':ok, 'safe_area':safe, 'problem': '' if ok else 'caption overlaps platform UI unsafe area'})
 return res

def main():
 p=argparse.ArgumentParser(description='Check burned-in video captions against platform safe areas.')
 p.add_argument('captions_json'); p.add_argument('--preset',choices=PRESETS,default='vertical-short'); p.add_argument('--frame',type=parse_frame,help='override frame size as WIDTHxHEIGHT'); p.add_argument('--unsafe',type=parse_unsafe,help='override unsafe margins as TOP,BOTTOM,LEFT,RIGHT'); p.add_argument('--json',action='store_true')
 a=p.parse_args(); caps=json.load(open(a.captions_json,encoding='utf-8'))
 try: res=check(caps,a.preset,a.frame,a.unsafe)
 except ValueError as e: p.error(str(e))
 if a.json: print(json.dumps({'preset':a.preset,'results':res,'unsafe_count':sum(not r['safe'] for r in res)},indent=2,ensure_ascii=False))
 else:
  for r in res: print(('OK  ' if r['safe'] else 'BAD ')+r['text']+' '+str(r['box'])+' '+r['problem'])
if __name__=='__main__': main()
