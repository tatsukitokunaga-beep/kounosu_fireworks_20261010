from pathlib import Path
from playwright.sync_api import sync_playwright
import json
OUT=Path(__file__).resolve().parent;HTML=(Path(__file__).resolve().parent.parent/'index.html').read_text();STUB=(Path(__file__).resolve().parent/'smoke.py').read_text().split("STUB=r'''",1)[1].split("'''",1)[0]
res=[];errs=[]
def check(n,v,d=None):res.append({'check':n,'passed':bool(v),'detail':d});print(('PASS' if v else 'FAIL'),n,d or '',flush=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-gpu'])
 c=b.new_context(viewport={'width':844,'height':390},device_scale_factor=1,is_mobile=True,has_touch=True);c.route('**/*',lambda r:r.abort());p=c.new_page();p.set_default_timeout(10000);p.on('pageerror',lambda e:errs.append(str(e)));p.evaluate(STUB);p.set_content(HTML,wait_until='domcontentloaded')
 p.evaluate("launchCelebration();clearSequence();setPhase('ready')");p.wait_for_timeout(100);p.locator('#playCelebrationVideo').click(force=True);p.wait_for_timeout(100);p.evaluate('fakePlayer.seekTo(9.55)');p.wait_for_timeout(750)
 d=p.evaluate('({s:lastSoundIndex,ctx:clinkAudio?.state,n:sounds.size,t:fakePlayer.getCurrentTime()})');check('glass_sound_scheduled_at_first_impact',d['s']==0,d)
 p.evaluate('fakePlayer.buffer()');check('buffer_cancels_audio_nodes',p.evaluate('sounds.size===0'))
 p.evaluate("fakePlayer.o.events.onAutoplayBlocked()");check('blocked_autoplay_explains_retry',p.locator('#movieAlert').is_visible())
 p.locator('#retryMovie').click(force=True);p.wait_for_timeout(80);check('retry_resumes_video',p.evaluate('playerState===1&&document.getElementById("movieAlert").hidden'),p.evaluate('({state:playerState,hidden:document.getElementById("movieAlert").hidden})'))
 p.evaluate('fakePlayer.o.events.onError({data:153})');check('embed_error_has_recovery',p.locator('#movieAlert').is_visible() and '公開URL' in p.locator('#movieAlertText').inner_text())
 p.locator('#closeCelebrationVideo').click(force=True);check('close_after_error_returns_site',p.evaluate("phase==='closed'&&!document.body.classList.contains('celebrating')"))
 # Reopen then cancel before playback, stale preparation must not reopen the UI.
 p.evaluate('launchCelebration();closeCelebration()');p.wait_for_timeout(200);check('rapid_reopen_cancel_no_stale_scene',p.evaluate("phase==='closed'&&!celebration.classList.contains('show')"))
 check('no_extra_exceptions',not errs,errs);b.close()
OUT.joinpath('extra_results.json').write_text(json.dumps(res,ensure_ascii=False,indent=2))
