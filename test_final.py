from pathlib import Path
from playwright.sync_api import sync_playwright
import json,math,time
OUT=Path(__file__).resolve().parent;HTML=(Path(__file__).resolve().parent.parent/'index.html').read_text()
STUB=(Path(__file__).resolve().parent/'smoke.py').read_text().split("STUB=r'''",1)[1].split("'''",1)[0]
STORE_STUB="""(() => {const mem=new Map();Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>mem.get(k)??null,setItem:(k,v)=>mem.set(k,String(v)),removeItem:k=>mem.delete(k),clear:()=>mem.clear()}});window.__local=mem})();"""
results=[];errors=[]
def check(name,value,detail=None):
 results.append({'check':name,'passed':bool(value),'detail':detail});print(('PASS ' if value else 'FAIL ')+name,detail or '',flush=True)
def ev(p,code):return p.evaluate(code)
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-gpu','--disable-dev-shm-usage'])
 c=b.new_context(viewport={'width':390,'height':844},device_scale_factor=1,is_mobile=True,has_touch=True)
 c.route('**/*',lambda r:r.abort())
 p=c.new_page();p.set_default_timeout(10000);p.on('pageerror',lambda e:errors.append(str(e)));p.evaluate(STORE_STUB);p.evaluate(STUB);p.set_content(HTML,wait_until='domcontentloaded');p.wait_for_timeout(200)
 check('script_initialization_23_items',p.locator('.check').count()==23)
 check('no_duplicate_ids',ev(p,"(()=>{const ids=[...document.querySelectorAll('[id]')].map(x=>x.id);return new Set(ids).size===ids.length})()"))
 for w,h in [(320,568),(375,667),(390,844),(430,932)]:
  p.set_viewport_size({'width':w,'height':h});p.wait_for_timeout(80)
  bounds=ev(p,"({w:innerWidth,sw:document.documentElement.scrollWidth})")
  check('portrait_no_overflow_'+str(w),bounds['sw']<=bounds['w'],bounds)
 p.set_viewport_size({'width':390,'height':844})
 # final must not fire early
 p.locator('[data-k="乾杯準備-0"]').evaluate('(e)=>e.click()')
 check('final_gate_before_preparation',ev(p,"state[FINAL_KEY]!==true&&phase==='closed'"))
 p.locator('[data-omit="お酒-3"]').evaluate('(e)=>e.click()')
 check('optional_wine_excluded',ev(p,"omitted('お酒-3')&&!state['お酒-3']"))
 check('save_change_queue',ev(p,"dirty['omit:お酒-3']===true"))
 ev(p,"document.getElementById('stopGps').click()")
 check('stop_gps_not_checklist_item',ev(p,"!Object.hasOwn(state,'omit:undefined')"))
 # clear / stored bool state integrity
 ev(p,"for(const k of prepKeys)if(!omitted(k)&&!state[k])document.querySelector('.check[data-k=\"'+k+'\"]').click()")
 check('ready_without_auto_kanpai',ev(p,"prepReady()&&phase==='closed'&&state[FINAL_KEY]!==true"))
 check('state_saved_to_storage',ev(p,"JSON.parse(localStorage.getItem(STORE))['服装-0']===true"))
 p.locator('[data-k="乾杯準備-0"]').evaluate('(e)=>e.click()');p.wait_for_timeout(1500)
 check('final_scroll_then_intro',ev(p,"phase==='intro'"),ev(p,'phase'))
 # no initial hand/body scroll reset trap
 p.locator('#cancelPreparation').evaluate('(e)=>e.click()');check('close_intro_restores_page',ev(p,"phase==='closed'&&!document.querySelector('.app').inert&&!document.body.classList.contains('celebrating')"))
 # Map fallback must load regardless of external scripts
 p.locator('#mapWrap').scroll_into_view_if_needed();p.wait_for_timeout(250)
 image=ev(p,"({ok:fallbackImg.complete&&fallbackImg.naturalWidth>0,w:fallbackImg.naturalWidth,h:fallbackImg.naturalHeight})")
 check('embedded_guide_loads_offline',image['ok'],image)
 check('map_default_scroll_priority',ev(p,"!mapInteraction&&getComputedStyle(fallback).touchAction==='pan-y'"))
 p.locator('#zoomIn').click(force=True);check('guide_zoom_in',ev(p,'gScale>1'))
 p.locator('#mapInteract').click(force=True);check('map_operable_only_when_enabled',ev(p,"mapInteraction&&getComputedStyle(fallback).touchAction==='none'"))
 for _ in range(12):p.locator('#zoomIn').click(force=True)
 check('guide_zoom_cap',ev(p,'gScale===5'))
 p.locator('#full').click(force=True);check('map_fullscreen_css',ev(p,"document.getElementById('mapWrap').classList.contains('full-map')"))
 p.locator('#full').click(force=True);check('map_exit_unlocks_scroll',ev(p,"!mapInteraction&&!document.body.classList.contains('map-expanded')"))
 p.locator('#realBtn').click(force=True);p.wait_for_timeout(450)
 check('map_unavailable_fallback_not_blank',ev(p,"getComputedStyle(fallback).display!=='none'&&fallbackImg.naturalWidth>0"))
 # Manual scene entry; use click dispatch to avoid testing-tool waiting on infinitely pulsing button
 p.locator('#cheers').evaluate('(e)=>e.click()');p.wait_for_timeout(6500)
 check('prep_portrait_no_primary_play_button',ev(p,"phase==='ready'&&document.getElementById('playCelebrationVideo').hidden"))
 for w,h in [(667,320),(844,390),(932,430)]:
  p.set_viewport_size({'width':w,'height':h});p.wait_for_timeout(80)
  rect=p.locator('#playCelebrationVideo').bounding_box()
  check('landscape_play_fits_'+str(w),rect and rect['x']>=0 and rect['y']>=0 and rect['x']+rect['width']<=w and rect['y']+rect['height']<=h,rect)
  check('one_primary_start_'+str(w),p.locator('#prepStage button:visible').count()==1)
 p.set_viewport_size({'width':844,'height':390});p.locator('#playCelebrationVideo').click(force=True);p.wait_for_timeout(180)
 check('movie_started',ev(p,"phase==='video'&&videoStarted&&playerState===1"))
 ev(p,'fakePlayer.seekTo(9)');p.wait_for_timeout(160)
 check('countdown_at_9_seconds',ev(p,"document.getElementById('digitLeft').textContent==='1'&&document.getElementById('digitRight').textContent==='1'"))
 ev(p,'fakePlayer.pauseVideo()')
 for w,h in [(667,320),(844,390),(932,430)]:
  p.set_viewport_size({'width':w,'height':h});p.wait_for_timeout(50);g=ev(p,'HanabiReview.poseAt(10)')
  check('glass_rims_contact_'+str(w),abs(g['gap']-2)<.01,g)
 p.set_viewport_size({'width':844,'height':390});g0=ev(p,'HanabiReview.poseAt(10)');g1=ev(p,'HanabiReview.poseAt(10.8)');g2=ev(p,'HanabiReview.poseAt(10+8*60/158)')
 check('glass_recoil_then_recontact',g1['gap']>300 and abs(g2['gap']-2)<.01)
 ev(p,'HanabiReview.poseAt(45)');check('cheers_persistent_45_seconds',ev(p,"+document.getElementById('cheersLeft').style.opacity===1&&+document.getElementById('cheersRight').style.opacity===1"))
 ev(p,'fakePlayer.seekTo(11.2);fakePlayer.playVideo()');p.wait_for_timeout(180);ev(p,'fakePlayer.pauseVideo()');a=ev(p,"document.getElementById('handLeft').style.transform");p.wait_for_timeout(300);bb=ev(p,"document.getElementById('handLeft').style.transform")
 check('pause_freezes_hand_motion',a==bb)
 check('pause_cancels_scheduled_sounds',ev(p,"HanabiReview.getState().activeSoundNodes===0&&!HanabiReview.getState().raf"))
 ev(p,'fakePlayer.playVideo()');p.wait_for_timeout(170);ev(p,'fakePlayer.buffer()');a=ev(p,"document.getElementById('handLeft').style.transform");p.wait_for_timeout(300);bb=ev(p,"document.getElementById('handLeft').style.transform");check('buffering_freezes_motion',a==bb)
 ev(p,'fakePlayer.seekTo(4);fakePlayer.playVideo()');p.wait_for_timeout(180);check('seek_backward_resets_count_and_cheers',ev(p,"document.getElementById('digitLeft').textContent==='6'&&+document.getElementById('cheersLeft').style.opacity===0"))
 ev(p,'fakePlayer.speed(1.5)');p.wait_for_timeout(80);check('rate_change_updates_clock',ev(p,'clock.rate===1.5'))
 ev(p,"document.getElementById('openSync').click();document.getElementById('syncEarlier').click()")
 check('timing_adjust_20ms',ev(p,'sceneSettings.offsetMs===-20'))
 ev(p,"document.getElementById('syncLater').click();document.getElementById('closeSync').click();document.getElementById('toggleSfx').click()")
 check('sfx_toggle_independent_music',ev(p,'sceneSettings.sfx===false&&playerState===1'))
 # quantised clock test across natural 250ms updates using its own fake sampled clock
 measured=ev(p,"""async()=>{const p0=performance.now();const fake={getCurrentTime:()=>Math.floor((performance.now()-p0)/250)*.25,getPlaybackRate:()=>1};const c=new MediaClock(fake);c.setRunning(true);const arr=[];for(let i=0;i<32;i++){await new Promise(r=>setTimeout(r,20));const wall=(performance.now()-p0)/1000;arr.push({e:c.read()-wall,t:c.last})}return {maxAbs:Math.max(...arr.map(x=>Math.abs(x.e))),monotonic:arr.every((x,i)=>!i||x.t>=arr[i-1].t)}}""")
 check('quantised_clock_monotonic',measured['monotonic'],measured)
 check('quantised_clock_error_under_150ms',measured['maxAbs']<.15,measured)
 p.locator('#closeCelebrationVideo').click(force=True);state=ev(p,'HanabiReview.getState()')
 check('close_releases_media_timers_audio',state['phase']=='closed' and state['activeSoundNodes']==0 and state['activeSequenceTimers']==0 and not state['raf'],state)
 # corruption cannot take down UI: new document with malformed persistent data
 p2=c.new_page();p2.on('pageerror',lambda e:errors.append(str(e)));p2.evaluate(STORE_STUB);p2.evaluate("localStorage.setItem('kounosu2026-check-hanabi-2026','{broken json')");p2.set_content(HTML,wait_until='domcontentloaded');p2.wait_for_timeout(150)
 check('corrupt_storage_recovery',p2.locator('.check').count()==23 and p2.evaluate('typeof launchCelebration==="function"'))
 p2.close();check('no_js_exceptions',len(errors)==0,errors)
 OUT.joinpath('test_results.json').write_text(json.dumps({'environment':'Chromium, touch mobile emulation; YouTube API mocked; external requests blocked; not iPhone device nor real audio verification','results':results,'errors':errors},ensure_ascii=False,indent=2))
 b.close()
print('TOTAL',len(results),'PASSED',sum(r['passed'] for r in results),flush=True)
