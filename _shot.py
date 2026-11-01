"""Isolate one section of the built dashboard and render it headless, so long
card copy can be eyeballed for overflow/wrapping."""
import pathlib

here = pathlib.Path(__file__).resolve().parent
src = (here / "ai_drone_dashboard.html").read_text(encoding="utf-8")

PROBES = {
    # keep only the section that owns the Alberta cards
    "albcards": """
      document.querySelectorAll('section.sec').forEach(function(s){
        if(!s.querySelector('#abCards')) s.style.display='none';
      });
      window.scrollTo(0,0);
    """,
    # keep only the global "how we use them" section
    "ucs": """
      document.querySelectorAll('section.sec').forEach(function(s){
        var g=s.querySelector('.uc-grid');
        if(!g || g.id==='abCards') s.style.display='none';
      });
      window.scrollTo(0,0);
    """,
}

for name, body in PROBES.items():
    inject = "<script>try{\n" + body + """
}catch(e){console.error(e);}
</script>"""
    html = src.replace("</body>", inject + "</body>", 1)
    (here / f"_probe_{name}.html").write_text(html, encoding="utf-8")
    print("wrote", f"_probe_{name}.html")
