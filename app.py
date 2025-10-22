<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>沖ドキツール</title>

<!-- ===============================
     🔹 OGP / Twitterカード設定
     =============================== -->
<meta property="og:type" content="website">
<meta property="og:title" content="沖ドキツール">
<meta property="og:description" content="沖ドキシリーズ専用のスロット分析ツール。REG/BIG履歴を入力すると差枚と有利Gを自動集計します。">
<meta property="og:url" content="https://kenkentools.com/okidoki/tools">
<meta property="og:image" content="https://kenkentools.com/static/okidoki.jpg">
<meta property="og:site_name" content="けんけんスロット分析ツール">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="沖ドキツール">
<meta name="twitter:description" content="沖ドキシリーズ専用のスロット分析ツール。REG/BIG履歴を入力すると差枚と有利Gを自動集計します。">
<meta name="twitter:image" content="https://kenkentools.com/static/okidoki.jpg">

<!-- ===============================
     🔹 Googleアナリティクス（GA4）
     =============================== -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-HXM85ZV043"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-HXM85ZV043');
</script>

<!-- ===============================
     🔹 スタイル（全体デザイン）
     =============================== -->
<style>
:root{
  --gap: 6px;
  --font: 14px;
  --maxw: 820px;
  --theme: #F7C948; /* 初期はゴールド */
}
*{box-sizing:border-box;}
body{
  font-family:system-ui,-apple-system,"Noto Sans JP",sans-serif;
  margin:14px;
  color:#222;
  font-size:var(--font);
}
.container{max-width:var(--maxw);margin:0 auto;}
h1{font-size:20px;margin:0 0 16px 0;padding-left:10px;border-left:6px solid var(--theme);}
.theme-bar{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px;}
.theme-btn{border:1px solid #ccc;border-radius:999px;padding:6px 10px;background:#fff;cursor:pointer;font-weight:600;}
.theme-btn[data-key="gold"]{background:#FFF6CF;}
.theme-btn[data-key="black"]{background:#e9e9e9;}
.theme-btn[data-key="gorgeous"]{background:#ffe5f0;}
.theme-btn.active{border-color:var(--theme);}
.controls{display:flex;gap:var(--gap);margin-top:10px;flex-wrap:wrap;}
button{padding:5px 8px;border:1px solid #ccc;border-radius:6px;background:#fff;cursor:pointer;}
table{width:100%;border-collapse:collapse;margin-top:10px;table-layout:fixed;}
th,td{border:1px solid #e5e5e5;padding:6px 4px;text-align:center;font-size:13px;}
thead th{background:#fafafa;}
th.col-label{width:12%;}
th.col-kind{width:25%;}
th.col-games{width:15%;}
th.col-yuuri{width:12%;}
th.col-diff{width:12%;}
th.col-ops{width:12%;}
.kind-btns{display:flex;justify-content:center;gap:6px;}
.kind-btns button{border:1px solid #ccc;border-radius:6px;padding:4px 8px;cursor:pointer;}
.kind-btns button.reg-selected{background:#1976d2;color:#fff;border-color:#1976d2;}
.kind-btns button.big-selected{background:#d32f2f;color:#fff;border-color:#d32f2f;}
input[type="number"]{width:100%;max-width:5em;padding:3px 4px;text-align:center;}
.value-text{display:inline-block;min-width:4em;text-align:center;}
.charts{margin-top:14px;}
.chart-card{padding:10px;border:2px solid var(--theme);border-radius:8px;background:#fff;height:600px;}
#chartScatter{width:100%;height:100%;display:block;}
.analytics{margin-top:14px;}
.card{border:1px solid #e5e5e5;border-radius:8px;padding:10px;background:#fff;}
.card h2{font-size:16px;margin:0 0 8px 0;padding-left:8px;border-left:4px solid var(--theme);}
.kpi-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;}
.kpi{border:1px solid #f0f0f0;border-radius:8px;padding:8px;background:#fafafa;}
.kpi .label{font-size:12px;color:#666;}
.kpi .value{font-size:18px;font-weight:700;}
.kpi .sub{font-size:12px;color:#888;}
</style>
</head>

<body>
<div class="container">
  <h1>沖ドキツール</h1>
  <div class="theme-bar">
    <button class="theme-btn" data-key="gold">ゴールド</button>
    <button class="theme-btn" data-key="black">ブラック</button>
    <button class="theme-btn" data-key="gorgeous">ゴージャス</button>
  </div>

  <div class="controls">
    <button id="add-row-btn">＋ 履歴を追加</button>
    <button id="reset-btn">リセット（初期10件）</button>
  </div>

  <table>
    <thead>
      <tr>
        <th class="col-label">履歴</th>
        <th class="col-kind">種別</th>
        <th class="col-games">ゲーム数</th>
        <th class="col-yuuri">有利G数</th>
        <th class="col-diff">差枚数</th>
        <th class="col-ops">操作</th>
      </tr>
    </thead>
    <tbody id="tbody"></tbody>
  </table>

  <section class="analytics">
    <div class="card">
      <h2>アナリティクス</h2>
      <div class="kpi-grid" id="kpi-grid"></div>
    </div>
  </section>

  <div class="charts">
    <div class="chart-card"><canvas id="chartScatter"></canvas></div>
  </div>
</div>

<!-- ===============================
     🔹 スクリプト本体
     =============================== -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script>
const THEMES={
  gold:{color:"#F7C948",yuuri:{REG:29,BIG:69}},
  black:{color:"#111111",yuuri:{REG:24,BIG:59}},
  gorgeous:{color:"#E91E63",yuuri:{REG:24,BIG:59}}
};
const KINDS=["REG","BIG"];
const FIXED_MEDALS={REG:90,BIG:210};
let FIXED_YUURI={...THEMES.gold.yuuri};
const DEFAULT_ROWS=Array.from({length:10},(_,i)=>({label:`${i+1}個目`,kind:"REG",games:""}));
const tbody=document.getElementById("tbody");
const toInt=v=>{const n=Number(v);return Number.isFinite(n)?Math.trunc(n):0;};
const floorInt=n=>Math.floor(Number(n)||0);

function buildRow(i,d){
  const tr=document.createElement("tr");
  tr.dataset.index=i;
  const td1=document.createElement("td");td1.textContent=d.label;
  const td2=document.createElement("td");const wrap=document.createElement("div");wrap.className="kind-btns";
  KINDS.forEach(k=>{
    const b=document.createElement("button");b.textContent=k;
    if(k===d.kind)b.classList.add(k==="REG"?"reg-selected":"big-selected");
    b.onclick=()=>{
      wrap.querySelectorAll("button").forEach(x=>x.classList.remove("reg-selected","big-selected"));
      b.classList.add(k==="REG"?"reg-selected":"big-selected");
      recalc();
    };
    wrap.appendChild(b);
  });
  td2.appendChild(wrap);
  const td3=document.createElement("td");const inp=document.createElement("input");inp.type="number";inp.value=d.games;inp.oninput=recalc;td3.appendChild(inp);
  const td4=document.createElement("td");const y=document.createElement("span");y.className="value-text";y.textContent="0";td4.appendChild(y);
  const td5=document.createElement("td");const m=document.createElement("span");m.className="value-text";m.textContent="0";td5.appendChild(m);
  const td6=document.createElement("td");const del=document.createElement("button");del.textContent="削除";del.onclick=()=>{tr.remove();renumber();recalc();};td6.appendChild(del);
  tr.append(td1,td2,td3,td4,td5,td6);
  tr._refs={inp,y,m,wrap,td1};
  tbody.appendChild(tr);
}
function renumber(){[...tbody.querySelectorAll("tr")].forEach((tr,i)=>tr._refs.td1.textContent=`${i+1}個目`);}
let chart;
function initChart(){
  const ctx=document.getElementById("chartScatter").getContext("2d");
  if(chart)chart.destroy();
  chart=new Chart(ctx,{type:"line",data:{datasets:[{data:[],showLine:true,borderColor:getComputedStyle(document.documentElement).getPropertyValue("--theme").trim(),tension:0.2,pointRadius:0}]},options:{responsive:true,maintainAspectRatio:false,scales:{x:{type:"linear",min:0,max:6000,title:{display:true,text:"総有利G数"}},y:{min:-6000,max:3000,title:{display:true,text:"総差枚数"}}},plugins:{legend:{display:false}}}});
}
const kpiGrid=document.getElementById("kpi-grid");
function setKPI(items){kpiGrid.innerHTML="";items.forEach(o=>{const d=document.createElement("div");d.className="kpi";d.innerHTML=`<div class="label">${o.label}</div><div class="value">${o.value}</div>${o.sub?`<div class='sub'>${o.sub}</div>`:""}`;kpiGrid.appendChild(d);});}
function recalc(){
  let xsum=0,ysum=0,totalG=0,totalCost=0,totalMedal=0,cREG=0,cBIG=0,rows=0;const pts=[{x:0,y:0}];
  [...tbody.querySelectorAll("tr")].forEach(tr=>{
    const {inp,y,m,wrap}=tr._refs;
    const sel=[...wrap.querySelectorAll("button")].find(b=>b.classList.contains("reg-selected")||b.classList.contains("big-selected"));
    const kind=sel?sel.textContent:"REG";const g=toInt(inp.value);
    const medal=FIXED_MEDALS[kind],yuuri=FIXED_YUURI[kind],cost=floorInt(g*(50/32));
    const xb=xsum+g,yb=ysum-cost;pts.push({x:xb,y:yb});const xa=xb+yuuri,ya=yb+medal;pts.push({x:xa,y:ya});
    y.textContent=xa;m.textContent=ya;xsum=xa;ysum=ya;totalG+=g;totalCost+=cost;totalMedal+=medal;kind==="REG"?cREG++:cBIG++;rows++;
  });
  if(!chart)initChart();chart.data.datasets[0].data=pts;chart.data.datasets[0].borderColor=getComputedStyle(document.documentElement).getPropertyValue("--theme").trim();chart.update();
  const eff=xsum>0?(ysum/xsum).toFixed(3):"-";const avgG=rows>0?(totalG/rows).toFixed(1):"-";
  setKPI([{label:"総有利G数",value:xsum},{label:"総差枚数（収支）",value:ysum,sub:`メダル ${totalMedal} / コスト ${totalCost}`},{label:"履歴件数",value:rows,sub:`REG ${cREG} / BIG ${cBIG}`},{label:"平均G/件",value:avgG},{label:"差枚効率(枚/有利G)",value:eff}]);
}
function addRow(){buildRow(tbody.children.length,{label:`${tbody.children.length+1}個目`,kind:"REG",games:""});recalc();}
function reset(){tbody.innerHTML="";DEFAULT_ROWS.forEach((r,i)=>buildRow(i,r));recalc();}
function applyTheme(k){const t=THEMES[k];document.documentElement.style.setProperty("--theme",t.color);FIXED_YUURI={...t.yuuri};document.querySelectorAll(".theme-btn").forEach(b=>b.classList.toggle("active",b.dataset.key===k));recalc();}
reset();initChart();applyTheme("gold");
document.querySelectorAll(".theme-btn").forEach(b=>b.onclick=()=>applyTheme(b.dataset.key));
document.getElementById("add-row-btn").onclick=addRow;
document.getElementById("reset-btn").onclick=reset;
</script>
</body>
</html>
