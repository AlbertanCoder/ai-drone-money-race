"""Build probe pages for headless verification: optional JS to drive the page
into a state, plus a global error trap drawn as a visible banner."""
import pathlib
import sys

here = pathlib.Path(__file__).resolve().parent
src = (here / "ai_drone_dashboard.html").read_text(encoding="utf-8")

PROBES = {
    # click the Alberta region tab, then park an Albertan year under the cursor
    "ab": """
      document.querySelector('#regionSeg button[data-region="alberta"]').click();
      showCross(12);
    """,
    # Alberta + linear scale, to prove the per-region Y domain works in both modes
    "ablin": """
      document.querySelector('#regionSeg button[data-region="alberta"]').click();
      document.querySelector('#scaleSeg button[data-mode="lin"]').click();
      showCross(6);
    """,
    # switch to Alberta then back to Global, to catch state leakage
    "roundtrip": """
      document.querySelector('#regionSeg button[data-region="alberta"]').click();
      document.querySelector('#regionSeg button[data-region="global"]').click();
      showCross(6);
    """,
    # synthesise a real drag across the plot -> should zoom via zoomToX
    "drag": """
      const r = svg.getBoundingClientRect();
      const y = r.top + r.height * 0.55;
      const send = function(t, x){
        svg.dispatchEvent(new PointerEvent(t, {
          clientX: x, clientY: y, bubbles: true,
          pointerType: 'mouse', button: 0, buttons: 1, pointerId: 1
        }));
      };
      send('pointerdown', r.left + r.width * 0.30);
      send('pointermove', r.left + r.width * 0.42);
      send('pointermove', r.left + r.width * 0.56);
      send('pointerup',   r.left + r.width * 0.56);
    """,
    # preset zoom then park a year inside it
    "zoom": """
      setZoom('history');
      showCross(4);
    """,
    # start playback so it is caught mid-run
    "play": """
      togglePlay();
    """,
}

HEAD = ("<script>window.__errs=[];"
        "window.addEventListener('error',function(e){"
        "window.__errs.push((e.message||'?')+' @ line '+(e.lineno||'?'));});</script>")

TAIL = """<script>
(function(){
  var b=document.createElement('div');
  b.style.cssText='position:fixed;bottom:0;left:0;right:0;z-index:99999;'
    +'font:12px monospace;padding:8px 12px;white-space:pre-wrap';
  if(window.__errs.length){
    b.style.background='#dc2626'; b.style.color='#fff';
    b.textContent='JS ERRORS ('+window.__errs.length+'):\\n'+window.__errs.join('\\n');
  } else {
    b.style.background='#065f46'; b.style.color='#fff';
    b.textContent='NO JS ERRORS';
  }
  document.body.appendChild(b);
})();
</script>"""

name = sys.argv[1] if len(sys.argv) > 1 else "ab"
body = PROBES[name]

inject = ("<script>try{\n" + body + """
}catch(e){
  var d=document.createElement('div');
  d.style.cssText='position:fixed;top:0;left:0;right:0;background:#dc2626;color:#fff;'
    +'padding:10px;z-index:9999;font:13px monospace';
  d.textContent='PROBE ERROR: '+e.message;
  document.body.appendChild(d);
}
</script>""")

out = here / f"_probe_{name}.html"
html = src.replace("</head>", HEAD + "</head>", 1).replace("</body>", inject + TAIL + "</body>", 1)
out.write_text(html, encoding="utf-8")
print(f"wrote {out.name}")
