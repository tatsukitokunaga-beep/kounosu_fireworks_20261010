from playwright.sync_api import sync_playwright
from pathlib import Path
import json,time
OUT=Path(__file__).resolve().parent
URL='http://127.0.0.1:8765/kounosu_hanabi_final_v21/index.html'
STUB=r'''(() => {
class P {
 constructor(id,o){this.o=o;this.base=0;this.start=performance.now();this.rate=1;this.state=5;this.dead=false;this.vol=0;this.quantum=0;this.id=id;
 const n=document.getElementById(id);n.innerHTML='<div style="width:100%;height:100%;display:grid;place-items:center;background:radial-gradient(ellipse at center,#293e53,#101c2d 44%,#04070c);color:#90a6bc;text-align:center;font:14px sans-serif"><div>映像エリア<br><small style="font-size:10px;opacity:.7">動作テスト・YouTube通信なし</small></div></div>';window.fakePlayer=this;setTimeout(()=>{if(!this.dead)o.events.onReady({target:this})},30);
 }
 getCurrentTime(){let t=this.base+(this.state===1?(performance.now()-this.start)/1000*this.rate:0);return this.quantum?Math.floor(t/this.quantum)*this.quantum:t}
 getPlaybackRate(){return this.rate}getPlayerState(){return this.state}
 playVideo(){if(this.dead)return;this.start=performance.now();this.state=1;this.o.events.onStateChange({data:1,target:this})}
 pauseVideo(){this.base=this.getCurrentTime();this.state=2;this.o.events.onStateChange({data:2,target:this})}
 seekTo(t){this.base=t;this.start=performance.now()}
 buffer(){this.base=this.getCurrentTime();this.state=3;this.o.events.onStateChange({data:3,target:this})}
 speed(r){this.base=this.getCurrentTime();this.start=performance.now();this.rate=r;this.o.events.onPlaybackRateChange({data:r})}
 unMute(){this.muted=false}setVolume(v){this.vol=v}destroy(){this.dead=true;document.getElementById(this.id)?.replaceChildren()}
}
window.YT={Player:P,PlayerState:{PLAYING:1,PAUSED:2,BUFFERING:3,ENDED:0,CUED:5}};
})();'''
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu'])
 context=browser.new_context(viewport={'width':390,'height':844},device_scale_factor=1,is_mobile=True,has_touch=True)
 context.add_init_script(STUB)
 context.route('**/*',lambda r:r.continue_() if r.request.url.startswith('http://127.0.0.1') or r.request.url.startswith('data:') else r.abort())
 page=context.new_page();page.set_default_timeout(10000);errs=[];page.on('pageerror',lambda e:errs.append(str(e)))
 page.evaluate(STUB);page.set_content((Path(__file__).resolve().parent.parent/'index.html').read_text(),wait_until='domcontentloaded');page.wait_for_timeout(800)
 print('loaded',page.title(),'checks',page.locator('.check').count(),'errors',errs)
 print('overflow',page.evaluate('({width:innerWidth,scroll:document.documentElement.scrollWidth})'))
 page.screenshot(path=str(OUT/'top.png'))
 print('map image',page.locator('#fallbackImg').evaluate('(e)=>({complete:e.complete,width:e.naturalWidth,height:e.naturalHeight})'))
 page.locator('#cheers').click(force=True);page.wait_for_timeout(6900)
 print('ready portrait',page.evaluate('HanabiReview.getState()'))
 page.screenshot(path=str(OUT/'ready_portrait.png'))
 page.set_viewport_size({'width':844,'height':390});page.wait_for_timeout(350)
 print('ready bounds',page.locator('#playCelebrationVideo').bounding_box())
 page.screenshot(path=str(OUT/'ready_landscape.png'))
 page.locator('#playCelebrationVideo').click(force=True);page.wait_for_timeout(500)
 print('playing',page.evaluate('HanabiReview.getState()'))
 page.evaluate('fakePlayer.pauseVideo();HanabiReview.poseAt(9)');page.screenshot(path=str(OUT/'countdown.png'))
 for t in [9,9.8,10,10.1,10.76,11.9,13.038]:
  print('pose',t,page.evaluate('(t)=>HanabiReview.poseAt(t)',t))
 page.evaluate('HanabiReview.poseAt(10)');page.screenshot(path=str(OUT/'contact.png'))
 page.evaluate('HanabiReview.poseAt(11.32)');page.screenshot(path=str(OUT/'cheers.png'))
 page.locator('#closeCelebrationVideo').click(force=True);print('closed',page.evaluate('HanabiReview.getState()'))
 print('errors',errs)
 OUT.joinpath('smoke_errors.json').write_text(json.dumps(errs))
 browser.close()
