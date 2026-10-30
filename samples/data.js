const ITEMS=[
 {id:'dragon',kind:'game',name:'まなびドラゴン',short:'ドラゴン',no:'第1作',color:'var(--mint)',logo:'../img/logo_dragon.webp',icon:'../img/logo_dragon.webp',mons:[],
  for:'小学4〜6年',desc:'勉強して竜を育て、ラスボスに挑む。学習×ローグライト。6教科1184問、1日3回まで。',url:'https://nochi-jpg.github.io/manabi-dragon/',btn:'あそぶ'},
 {id:'battle',kind:'game',name:'まなびバトル',short:'バトル',no:'第2作・いちおし',color:'var(--pk)',logo:'../img/logo_battle.webp',icon:'../img/m_all.webp',mons:['m_kokugo','m_all','m_rika'],
  for:'小学4〜6年',desc:'5教科2500問に答えてモンスターを育て、ボスと戦う。友だちとQRで1台対戦。キャラはぜんぶ手描き。',url:'https://nochi-jpg.github.io/manabato/',btn:'あそぶ'},
 {id:'stadium',kind:'game',name:'まなびスタジアム',short:'スタジアム',no:'第3作・先生用',color:'var(--pur)',logo:'../img/logo_stadium.webp',icon:'../img/m_sansu.webp',mons:['m_sansu','m_eigo','m_shakai'],
  for:'先生用（電子黒板）',desc:'子どもの まなびバトルのQRを読みこんで、大画面で3Dの対戦を上映。クラス大会に。',url:'https://nochi-jpg.github.io/manasuta/',btn:'ひらく'},
 {id:'historia',kind:'game',name:'まなびヒストリア',short:'ヒストリア',no:'第4作',color:'var(--shu)',logo:'../img/logo_historia.webp',paper:true,icon:'../img/h_yuuki.webp',mons:['h_yuuki','h_honjii','h_tokei'],
  for:'小学6年・社会',desc:'タイムスリップして、ゆがめられた日本の歴史を正す。証言のおかしなところに「カード」をつきつける、歴史の追体験ゲーム。',url:'https://nochi-jpg.github.io/manabi-historia/',btn:'あそぶ'},
 {id:'life',kind:'game',name:'まなびライフ',short:'ライフ',no:'第5作',color:'var(--sky)',logo:'../img/life_title.webp',paper:true,icon:'../img/life_title.webp',iconPaper:true,mons:[],
  for:'小学5・6年・キャリア教育',desc:'日本のどこかに生まれた1人の人生を、0歳から最期まで。公的な統計にもとづく、超リアル人生シミュレーター。',url:'https://nochi-jpg.github.io/manabi-life/play/',btn:'あそぶ'},
 {id:'keisan',kind:'tool',name:'計算おたすけ君',short:'計算',no:'おたすけツール',color:'var(--ora)',ttl:'計算<br>おたすけ君',iconTxt:'計算',mons:['otasuke_chara'],
  for:'小学1年・計算',desc:'ブロック・数の線・さくらんぼで、くり上がり・くり下がりの考え方をおたすけ。問題に挑戦するモードもあり。',url:'https://nochi-jpg.github.io/otasuke-keisan/',btn:'つかう'},
 {id:'hissan',kind:'tool',name:'ひっ算おたすけ君',short:'ひっ算',no:'おたすけツール',color:'var(--teal)',ttl:'ひっ算<br>おたすけ君',iconTxt:'ひっ算',mons:['otasuke_chara'],
  for:'筆算',desc:'たし算・ひき算・かけ算・わり算の筆算を、答えは言わずに1段ずつおたすけ。さくらんぼ法や九九の表も見られる。',url:'https://daizou.my.canva.site/otasuke',btn:'つかう'},
 {id:'shousu',kind:'tool',name:'ひっ算おたすけ君（小数点あり）',short:'小数ひっ算',no:'おたすけツール',color:'var(--navy)',ttl:'ひっ算<br>おたすけ君<small>小数点あり版</small>',iconTxt:'小数<br>ひっ算',mons:['otasuke_chara'],
  for:'小数の筆算',desc:'ひっ算おたすけ君の、小数点がある計算に使える版。',url:'https://daizou.my.canva.site/otasukeshosu',btn:'つかう'}
];
const GROUPS={game:{label:'ゲーム',color:'var(--game)',lead:'あそびながら 勉強する'},tool:{label:'おたすけツール',color:'var(--tool)',lead:'授業や宿題で つかう'}};
const byKind=k=>ITEMS.filter(x=>x.kind===k);
const mk=(t,c,txt)=>{const e=document.createElement(t); if(c) e.className=c; if(txt!=null) e.textContent=txt; return e};
function fillCard(card,g){
  card.style.setProperty('--c',g.color); card.innerHTML='';
  const art=mk('div','art');
  if(g.logo){const lg=mk('img',g.paper?'logo paper':'logo'); lg.src=g.logo; lg.alt=g.name+' ロゴ'; art.append(lg);} else {const t=mk('div','ttl'); t.innerHTML='<span>'+g.ttl+'</span>'; art.append(t);}
  if(g.mons.length){const m=mk('div','mons'); g.mons.forEach(k=>{const im=mk('img'); im.src='../img/'+k+'.webp'; im.alt=''; m.append(im)}); art.append(m)} else art.classList.add('solo');
  const btns=mk('div','btns'); const a=mk('a','go',g.btn+' ▶'); a.href=g.url; a.target='_blank'; a.rel='noopener'; btns.append(a);
  card.append(mk('span','badge',g.no+'｜'+g.for),art,mk('h2',null,g.name),mk('p','desc',g.desc),btns);
  card.classList.remove('pop'); void card.offsetWidth; card.classList.add('pop');
}
function makeTile(g,tag){
  const t=mk(tag||'button','tile'); t.style.setProperty('--c',g.color);
  if(g.iconTxt){const d=mk('div','ic txt'); d.innerHTML=g.iconTxt; t.append(d)} else {const im=mk('img','ic'+(g.iconPaper?' paper':'')); im.src=g.icon; im.alt=''; t.append(im)}
  t.append(mk('b',null,g.short)); return t;
}
function smpBar(on){const d=mk('nav','smp'); d.append('見本'); [['a','A 切りかえ'],['b','B 入口'],['c','C 一覧']].forEach(([k,l])=>{const a=mk('a',k===on?'on':'',l); a.href=k+'.html'; d.append(a)}); return d}
function swipe(el,fn){let sx=null; el.addEventListener('touchstart',e=>{sx=e.touches[0].clientX},{passive:true}); el.addEventListener('touchend',e=>{if(sx==null)return; const dx=e.changedTouches[0].clientX-sx; if(Math.abs(dx)>40) fn(dx<0?1:-1); sx=null})}
