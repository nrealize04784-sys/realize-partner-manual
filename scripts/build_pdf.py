from pathlib import Path
from bs4 import BeautifulSoup
from weasyprint import HTML

src = Path("manual-base.html")
out = Path("REALIZE_CLUB_Manual.pdf")
soup = BeautifulSoup(src.read_text(encoding="utf-8"), "html.parser")
market = soup.find("section", id="market")
if market:
    for note in market.find_all("div", class_="note"):
        if note.get_text(" ", strip=True).startswith("お買い物画面の確認"):
            note.decompose()

css = r"""
@page { size:A4; margin:15mm 15mm 17mm 15mm;
  @bottom-right { content: counter(page) " / " counter(pages); color:#708477; font:8.6pt "Noto Sans CJK JP",sans-serif; }
  @bottom-left { content:"REALIZE PARTNER  |  REALIZE CLUB"; color:#819289; font:7.5pt "Noto Sans CJK JP",sans-serif; }
}
@page:first { @bottom-left {content:none;} @bottom-right {content:none;} }
@media print {
  .manualSection,.manualSection#overview,.manualSection#rpstart,.manualSection#contract,
  .manualSection#line,.manualSection#portal,.manualSection#mio,.manualSection#market,
  .manualSection#follow,.manualSection#check {break-before:auto!important;page-break-before:auto!important;}
  .manualSection{margin-bottom:5mm!important;}
  .sectionHead{break-after:avoid!important;page-break-after:avoid!important;margin-top:4mm;}
  .manualSection .articleBody{padding-bottom:1.5mm;}
  .articleBody h3{break-after:avoid!important;margin-top:4mm;}
  .hero{break-after:page!important;page-break-after:always!important;}
  .screenflow{display:block!important;}
  .screenstep,.screenstep:has(.shot-landscape),.screenstep:has(.two-images){
    display:grid!important;grid-template-columns:minmax(0,1fr) minmax(0,48%)!important;
    column-gap:4mm!important;padding:2.5mm 0!important;margin:0!important;
    break-inside:avoid!important;page-break-inside:avoid!important;
  }
  .screenstep.no-image{display:block!important;}
  .screenstep-photos,.screenstep:has(.shot-landscape) .screenstep-photos{width:100%!important;max-width:100%!important;}
  .screenstep-photos .shot{padding:1.3mm!important;}
  .screenstep-photos .shot img{max-height:67mm!important;height:auto!important;max-width:100%!important;}
  .screenstep-photos .shot-landscape img{max-height:53mm!important;}
  .screenstep .shot-landscape img{max-height:53mm!important;}
  .screenstep-photos.two-images{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:1.5mm!important;}
  .screenstep-photos.two-images .shot img{max-height:70mm!important;}
  .screenstep-text{grid-template-columns:7.6mm minmax(0,1fr)!important;gap:2.3mm!important;}
  .screenstep-text h4{font-size:10.5pt!important;}
  .screenstep-text p{font-size:9.6pt!important;line-height:1.58!important;}
  .screenstep-photos .shot figcaption{font-size:7.6pt!important;line-height:1.35!important;}
  .service-guide{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:2.5mm!important;}
  .sg-card{padding:2.5mm 3mm!important;}
  .sg-card p{font-size:8.5pt!important;}
  .quickcards>div,.tilegrid>div,.sourcegrid>div{break-inside:avoid;}
  .note{break-inside:avoid;}
  .step{break-inside:avoid;}
  .articleBody table{margin:2mm 0 3mm;}
}
"""
soup.style.append(css)
HTML(string=str(soup), base_url=".").write_pdf(str(out))
print(f"Generated {out} ({out.stat().st_size} bytes)")
