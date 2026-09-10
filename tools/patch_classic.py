from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
if 'id="classicScript"' in s:
    print('classic selector already present')
    raise SystemExit(0)

s=s.replace('.ghost{border:1px solid var(--line);background:white;color:var(--ink);border-radius:10px;padding:8px 11px}.primary', '.ghost{border:1px solid var(--line);background:white;color:var(--ink);border-radius:10px;padding:8px 11px}.script-select{min-width:150px;padding:8px 10px;border:1px solid var(--line);border-radius:10px;background:#fff;color:var(--ink)}.primary')
s=s.replace('.players{display:flex;flex-direction:column;gap:7px}.player{display:grid;grid-template-columns:36px minmax(72px,1fr) auto 28px auto;', '.players{display:flex;flex-direction:column;gap:7px}.player{display:grid;grid-template-columns:36px minmax(72px,1fr) 24px auto 28px auto;')
s=s.replace('.role{width:100%;min-width:0;border:0;outline:0;padding:6px 2px;background:transparent;font-size:14px}.role.masked', '.role{width:100%;min-width:0;border:0;outline:0;padding:6px 2px;background:transparent;font-size:14px}.role-info-btn{width:22px;height:22px;border:0;border-radius:50%;background:var(--soft);color:#6f6960;font-size:12px;font-weight:900;padding:0;display:grid;place-items:center}.role-info-btn:disabled{opacity:.18;cursor:default}.role.masked')
s=s.replace('.role-pool-empty{font-size:12px;color:var(--muted)}.import-msg', '.role-pool-empty{font-size:12px;color:var(--muted)}.role-modal{position:fixed;inset:0;z-index:80;background:rgba(25,22,19,.42);display:none;align-items:center;justify-content:center;padding:18px}.role-modal.open{display:flex}.role-modal-box{width:min(460px,100%);background:var(--paper);border:1px solid var(--line);border-radius:16px;box-shadow:0 20px 60px rgba(20,16,12,.22);padding:18px}.role-modal-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px}.role-modal-name{font-size:20px;font-weight:900}.role-modal-team{font-size:12px;color:var(--muted);margin-top:3px}.role-modal-close{border:0;background:transparent;font-size:22px;color:var(--muted);padding:0 2px}.role-modal-ability{margin-top:14px;line-height:1.6;font-size:14px;white-space:pre-wrap}.role-modal-id{margin-top:12px;font-size:11px;color:var(--muted)}.import-msg')
s=s.replace('.player{grid-template-columns:34px minmax(60px,1fr) auto 25px auto;', '.player{grid-template-columns:34px minmax(58px,1fr) 22px auto 25px auto;')

old='''          <div><span class="small-label">我的号码</span><input class="number" id="mySeat" type="number" min="1" max="30" placeholder="空"></div>\n          <button class="ghost" id="clearAll" type="button">新开一局</button>'''
new='''          <div><span class="small-label">我的号码</span><input class="number" id="mySeat" type="number" min="1" max="30" placeholder="空"></div>\n          <div><span class="small-label">经典板子</span><select class="script-select" id="classicScript"><option value="">自由模式</option><option value="tb">暗流涌动</option><option value="custom">自定义 JSON</option></select></div>\n          <label class="file-btn">导入自定义 JSON<input id="scriptFile" type="file" accept=".json,application/json"></label>\n          <button class="ghost" id="clearAll" type="button">新开一局</button>'''
if old not in s: raise SystemExit('setup marker missing')
s=s.replace(old,new)

start=s.find('      <section class="card script-card" id="scriptCard">')
if start<0: raise SystemExit('script card missing')
end=s.find('      </section>',start)
endline=s.find('\n',end+len('      </section>'))
s=s[:start]+s[endline+1:]

modal='''\n  <div class="role-modal" id="roleModal" aria-hidden="true">\n    <div class="role-modal-box">\n      <div class="role-modal-head">\n        <div><div class="role-modal-name" id="roleModalName"></div><div class="role-modal-team" id="roleModalTeam"></div></div>\n        <button class="role-modal-close" id="roleModalClose" type="button">×</button>\n      </div>\n      <div class="role-modal-ability" id="roleModalAbility"></div>\n      <div class="role-modal-id" id="roleModalId"></div>\n    </div>\n  </div>\n'''
s=s.replace('  <datalist id="roleOptions"></datalist>',modal+'  <datalist id="roleOptions"></datalist>')
s=s.replace('script:null,scriptCollapsed:true,lastRoleSeat:0};', "script:null,scriptCollapsed:true,lastRoleSeat:0,classicScript:''};")
s=s.replace('state.scriptCollapsed=state.scriptCollapsed!==false;state.lastRoleSeat=Number(state.lastRoleSeat)||0;', "state.scriptCollapsed=state.scriptCollapsed!==false;state.lastRoleSeat=Number(state.lastRoleSeat)||0;state.classicScript=state.classicScript||((state.script&&state.script.name)?'custom':'');")
s=s.replace("document.getElementById('setupSummaryText').textContent=state.playerCount+'人 · '+state.config.map(Number).join(' / ')+(state.mySeat?' · 我:'+state.mySeat:'');", "document.getElementById('setupSummaryText').textContent=(state.script&&state.script.name?state.script.name+' · ':'')+state.playerCount+'人 · '+state.config.map(Number).join(' / ')+(state.mySeat?' · 我:'+state.mySeat:'');")

a=s.find('function renderScript(){')
b=s.find('function renderAll(){',a)
if a<0 or b<0: raise SystemExit('renderScript marker missing')
replacement='''function renderScript(){\n  const opts=document.getElementById('roleOptions');\n  const sel=document.getElementById('classicScript');\n  if(sel)sel.value=state.classicScript||'';\n  if(!state.script){opts.innerHTML='';return;}\n  opts.innerHTML=(state.script.roles||[]).map(r=>'<option value="'+esc(r.name)+'"></option>').join('');\n}\nfunction findRoleInfo(text){\n  const v=String(text||'').trim();\n  if(!v||!state.script)return null;\n  const low=v.toLowerCase();\n  return (state.script.roles||[]).find(r=>String(r.name||'').trim()===v || String(r.id||'').toLowerCase()===low) || null;\n}\nfunction teamName(team){return team==='townsfolk'?'镇民':team==='outsider'?'外来者':team==='minion'?'爪牙':team==='demon'?'恶魔':team||''}\nfunction showRoleInfo(role){\n  if(!role)return;\n  document.getElementById('roleModalName').textContent=role.name||role.id||'角色';\n  document.getElementById('roleModalTeam').textContent=teamName(role.team);\n  document.getElementById('roleModalAbility').textContent=role.ability||'这个 JSON 没有提供角色能力说明。';\n  document.getElementById('roleModalId').textContent=role.id?'ID: '+role.id:'';\n  const modal=document.getElementById('roleModal');modal.classList.add('open');modal.setAttribute('aria-hidden','false');\n}\nfunction closeRoleInfo(){const modal=document.getElementById('roleModal');modal.classList.remove('open');modal.setAttribute('aria-hidden','true')}\nasync function loadClassicScript(key){\n  if(!key){state.classicScript='';state.script=null;save();renderAll();return;}\n  if(key==='custom'){return;}\n  try{\n    const res=await fetch('data/trouble-brewing.json',{cache:'no-store'});\n    if(!res.ok)throw new Error('HTTP '+res.status);\n    state.script=parseScript(await res.json());state.classicScript='tb';save();renderAll();\n  }catch(err){alert('经典板子加载失败：'+err.message)}\n}\n'''
s=s[:a]+replacement+s[b:]

target='''      '<input class="role '+(state.hideRoles?'masked':'')+'" list="roleOptions" data-role="'+i+'" value="'+esc(displayRole)+'" placeholder="身份" '+(state.hideRoles?'readonly':'')+'>'+\n      '<button class="state-tag '+judge+'" type="button" data-judge-cycle="'+i+'">'+judgeLabel(judge)+'</button>'+'''
repl='''      '<input class="role '+(state.hideRoles?'masked':'')+'" list="roleOptions" data-role="'+i+'" value="'+esc(displayRole)+'" placeholder="身份" '+(state.hideRoles?'readonly':'')+'>'+\n      '<button class="role-info-btn" type="button" data-role-info="'+i+'" '+((!state.hideRoles&&findRoleInfo(realRole))?'':'disabled')+' title="查看角色能力">i</button>'+\n      '<button class="state-tag '+judge+'" type="button" data-judge-cycle="'+i+'">'+judgeLabel(judge)+'</button>'+'''
if target not in s: raise SystemExit('player role marker missing')
s=s.replace(target,repl)
s=s.replace("e.oninput=x=>{if(state.hideRoles)return;state.roles[x.target.dataset.role]=x.target.value;save()}", "e.oninput=x=>{if(state.hideRoles)return;state.roles[x.target.dataset.role]=x.target.value;save()};e.onchange=x=>{if(state.hideRoles)return;state.roles[x.target.dataset.role]=x.target.value;save();renderPlayers()}")
needle="  box.querySelectorAll('[data-status]').forEach(e=>e.onclick=x=>{const n=x.currentTarget.dataset.status;state.dead[n]=!state.dead[n];save();renderPlayers()});"
if needle not in s: raise SystemExit('status marker missing')
s=s.replace(needle,"  box.querySelectorAll('[data-role-info]').forEach(e=>e.onclick=x=>{if(state.hideRoles)return;const n=x.currentTarget.dataset.roleInfo;showRoleInfo(findRoleInfo(state.roles[n]||''))});\n"+needle)
s=s.replace("document.getElementById('scriptToggle').onclick=()=>{state.scriptCollapsed=!state.scriptCollapsed;save();renderScript()};\n",'')
s=s.replace("try{const data=JSON.parse(reader.result);state.script=parseScript(data);state.scriptCollapsed=false;save();renderScript()}", "try{const data=JSON.parse(reader.result);state.script=parseScript(data);state.classicScript='custom';save();renderAll()}")
marker="document.getElementById('scriptFile').onchange=e=>{"
if marker not in s: raise SystemExit('scriptFile marker missing')
s=s.replace(marker,"document.getElementById('classicScript').onchange=e=>loadClassicScript(e.target.value);\ndocument.getElementById('roleModalClose').onclick=closeRoleInfo;\ndocument.getElementById('roleModal').onclick=e=>{if(e.target.id==='roleModal')closeRoleInfo()};\n"+marker)
s=s.replace('script:null,scriptCollapsed:true,lastRoleSeat:0};', "script:null,scriptCollapsed:true,lastRoleSeat:0,classicScript:''};")

p.write_text(s,encoding='utf-8')
print('patched')
