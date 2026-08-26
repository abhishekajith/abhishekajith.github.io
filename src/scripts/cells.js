/* ════════════════════════ JAVASCRIPT GUIDE ════════════════════════
   Three independent features live here:
     A. toggleTheme()  - light/dark switch
     B. Cell system    - the living-cells canvas animation
     C. Reveal system  - fade-in-on-scroll
   ★EDIT-CELLS marks every number that is safe to tweak.           */

/* ──────────────── A. THEME TOGGLE ──────────────── */
/* Flips the .dark class on <body>; CSS variables do the rest.
   Then re-tints every existing cell so the canvas matches instantly
   (otherwise cells would keep the old theme's colours until they
   happened to divide).                                            */
function toggleTheme(){document.body.classList.toggle('dark');
  const p=pal();cells.forEach(c=>c.c=rndPal(p));}

/* ──────────────── B1. CANVAS SETUP ──────────────── */
const cv=document.getElementById('cells'),ctx=cv.getContext('2d');
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
/* If the visitor asked their OS for "reduce motion", we draw ONE
   static frame and skip all looping - accessibility requirement.  */

let W,H,          /* canvas size in CSS pixels            */
    DPR,          /* devicePixelRatio → sharpness on retina */
    cells=[],     /* every living cell object lives here   */
    mouse={x:-9999,y:-9999},   /* cursor pos; off-screen default */
    lastDiv=0,    /* timestamp of the last mitosis event   */
    nextDiv=1200; /* ms until the NEXT division is allowed
                     ★EDIT-CELLS smaller = divisions start sooner */

/* Colour sets per theme: [hue, saturation%, lightness%] triples.
   Light mode = deeper tones so pale cells stay visible on white;
   dark mode  = brighter, slightly desaturated glows.
   ★EDIT-CELLS change hues here (0=red · 120=green · 180=teal).   */
const PALETTES={
  light:[[168,52,46],[140,40,44],[96,48,54]],
  dark :[[160,60,56],[130,50,54],[92,55,64]]
};
function pal(){return document.body.classList.contains('dark')?PALETTES.dark:PALETTES.light;}
function rndPal(p){return p[Math.floor(Math.random()*p.length)];}  /* pick one at random */

/* ──────────────── B2. THE CELL OBJECT ──────────────── */
function Cell(x,y,r,c){
  this.x=x; this.y=y;        /* current position      */
  this.r=r; this.br=r;       /* radius + resting radius ("breath" target) */
  this.c=c.slice();          /* own copy of its colour triple     */
  const a=Math.random()*Math.PI*2,          /* random drift angle  */
        s=.06+Math.random()*.1;             /* drift speed px/frame ★EDIT-CELLS */
  this.vx=Math.cos(a)*s; this.vy=Math.sin(a)*s;
  this.ph=Math.random()*Math.PI*2;          /* phase offset so cells don't breathe in sync */
  this.bs=.0006+Math.random()*.0012;        /* breathing speed  ★EDIT-CELLS */
  this.ax=null;              /* division axis - null = not dividing */
  this.dt=0;                 /* seconds elapsed since division began */
}

/* Fill the dish. Count adapts to screen width:
   desktop 28 · tablet/phone 18 · reduced-motion 10. ★EDIT-CELLS  */
function spawn(n){
  const p=pal();
  for(let i=0;i<n;i++)
    cells.push(new Cell(Math.random()*W,Math.random()*H,22+Math.random()*48,rndPal(p)));}
                                 /* ↑ radius range px ★EDIT-CELLS */

/* Match canvas resolution to screen sharpness (retina crispness). */
function resize(){DPR=Math.min(devicePixelRatio||1,2);
  W=cv.offsetWidth;H=cv.offsetHeight;cv.width=W*DPR;cv.height=H*DPR;ctx.setTransform(DPR,0,0,DPR,0,0);}

/* ──────────────── B3. ONE ANIMATION FRAME ────────────────
   Runs ~60× per second. Order of work:
   1) maybe trigger a mitosis   2) clear canvas   3) move+draw each  */
function step(t){
  /* MITOSIS TIMER - when enough time passed AND population is under
     the cap (36 desktop / 22 phone), pick a random idle cell and
     give it a random division axis. ★EDIT-CELLS both numbers.      */
  if(!reduced&&t-lastDiv>nextDiv&&cells.length<(W<700?22:36)){
    lastDiv=t;nextDiv=1500+Math.random()*1100;   /* next window 1.5-2.6s */
    const c=cells[Math.floor(Math.random()*cells.length)];
    if(c&&c.ax==null){c.ax=Math.random()*Math.PI*2;c.dt=0;}
  }
  ctx.clearRect(0,0,W,H);        /* wipe previous frame */
  const dark=document.body.classList.contains('dark');

  for(let i=cells.length-1;i>=0;i--){const c=cells[i];

    /* CURSOR REACTION: inside a 170px radius a cell is gently pushed
       away - strength fades linearly to zero at the edge. Feel =
       stirring a petri dish. ★EDIT-CELLS radius & push force .05.  */
    let dx=c.x-mouse.x,dy=c.y-mouse.y,d=Math.hypot(dx,dy);
    if(d<170&&d>0){const f=(1-d/170)*.05;c.vx+=dx/d*f;c.vy+=dy/d*f;}

    c.vx*=.985;c.vy*=.985;       /* friction so pushes settle down */
    c.x+=c.vx;c.y+=c.vy;

    /* WRAP-AROUND: drifting off one edge re-enters from the other,
       keeping the dish permanently populated.                      */
    if(c.x<-90)c.x=W+90;if(c.x>W+90)c.x=-90;
    if(c.y<-90)c.y=H+90;if(c.y>H+90)c.y=-90;

    /* DIVIDING STATE: over 1.6s the cell pinches into two lobes that
       slide apart along its axis, then it is replaced by two real
       daughter cells with averaged colour. k goes 0→1.             */
    if(c.ax!=null){
      c.dt+=.016;                                   /* ≈ one frame */
      const k=Math.min(c.dt/1.6,1),off=k*c.br*.85,cr=c.br*(1-k*.28);
      const ox=Math.cos(c.ax)*off,oy=Math.sin(c.ax)*off;
      lobe(c.x-ox,c.y-oy,cr,c.c,k,dark);lobe(c.x+ox,c.y+oy,cr,c.c,k,dark);
      if(k>=1){cells.splice(i,1);                   /* parent dies…   */
        cells.push(new Cell(c.x-Math.cos(c.ax)*off,c.y-Math.sin(c.ax)*off,cr,mix(c.c)));
        cells.push(new Cell(c.x+Math.cos(c.ax)*off,c.y+Math.sin(c.ax)*off,cr,mix(c.c)));}
        /* …two daughters born, offset along the same axis.         */
      continue;                     /* skip normal drawing below    */
    }

    /* NORMAL STATE: radius oscillates ±7% around rest size - the
       "breathing". Then draw as one soft lobe.                     */
    c.r=c.br*(1+.07*Math.sin(t*c.bs+c.ph));
    lobe(c.x,c.y,c.r,c.c,null,dark);
  }
}
/* Blend a daughter's colour halfway between parent and a fresh
   palette pick - keeps the colony varied but harmonious.           */
function mix(c){const t=rndPal(pal());return[t[0],(c[1]+t[1])/2,(c[2]+t[2])/2];}

/* DRAW ONE CELL - three layered radial gradients:
   outer glow → body → tiny darker "nucleus" dot in the centre.
   alpha is deliberately low (.10-.15) so overlapping cells stay
   subtle. ★EDIT-CELLS raise alpha for bolder cells.                */
function lobe(x,y,r,c,k,dark){
  const[h,s,l]=c,alpha=(dark?.15:.10)*(k==null?1:(1-.3*Math.abs(k-.5)));
  const g=ctx.createRadialGradient(x,y,r*.15,x,y,r);
  g.addColorStop(0,`hsla(${h},${s}%,${l}%,${alpha})`);
  g.addColorStop(.75,`hsla(${h},${s}%,${l}%,${alpha*.45})`);
  g.addColorStop(1,`hsla(${h},${s}%,${l}%,0)`);       /* fades to nothing */
  ctx.fillStyle=g;ctx.beginPath();ctx.arc(x,y,r,0,7);ctx.fill();
  ctx.fillStyle=`hsla(${h},${s}%,${l}%,${alpha*.9})`;               /* nucleus */
  ctx.beginPath();ctx.arc(x,y,r*.16,0,7);ctx.fill();
}

/* ──────────────── B4. BOOT SEQUENCE ──────────────── */
resize();spawn(reduced?10:(W<700?18:28));                 /* first paint */
addEventListener('resize',()=>{resize();});               /* keep crisp  */
if(reduced){step(1000);}                                  /* static frame only */

/* Track the cursor RELATIVE to the hero so cells react only there. */
cv.parentElement.addEventListener('pointermove',e=>{const b=cv.getBoundingClientRect();
  mouse.x=e.clientX-b.left;mouse.y=e.clientY-b.top;});
cv.parentElement.addEventListener('pointerleave',()=>{mouse.x=-9999;mouse.y=-9999;});

/* THE LOOP - requestAnimationFrame calls step() once per display
   refresh (~60fps) and passes a millisecond timestamp as t.        */
if(!reduced){(function loop(t){step(t||0);requestAnimationFrame(loop)})(0);}

/* ──────────────── C. REVEAL ON SCROLL ────────────────
   Watches every element carrying class="rv". When ≥15% of it
   enters the viewport we add .visible (CSS then fades/slides it
   in) and stop watching - each element animates only once.        */
const io=new IntersectionObserver(es=>es.forEach(e=>{
  if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target);}}),{threshold:.15});
document.querySelectorAll('.rv').forEach(el=>io.observe(el));

/* The nav button can't use inline onclick inside bundled modules, */
/* so we attach it here. Everything else works exactly as before.  */
const __tb=document.getElementById('theme-btn');
if(__tb)__tb.addEventListener('click',toggleTheme);
