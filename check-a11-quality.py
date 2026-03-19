#!/usr/bin/env python3
"""
Umfassendes Qualitäts-Prüfskript für A1.1 NEW DaF-HTML-Dateien.
Prüft ALLE Regeln aus den verbindlichen Skills:
- Layout (daf-html-layout)
- Timer/Buttons (timer-bar, btn-row)
- Satzbau (satzbau-drag-drop)
- Übungsformen (daf-uebungsformen)
- Wortschatz-Tab (falls vorhanden)
- Bilder-Pflicht (daf-bilder-pflicht)
- Kein Prüfen-Button
- Keine "Satz 1/2/3"-Labels
- Keine doppelten Footer
- Korrekte DOM-IDs für Timer
"""

import re
import sys
import os
import glob

# ─── Farben ───────────────────────────────────────────────
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BOLD = '\033[1m'
RESET = '\033[0m'

def ok(msg):
    return f"  {GREEN}✓{RESET} {msg}"

def fail(msg):
    return f"  {RED}✗{RESET} {msg}"

def warn(msg):
    return f"  {YELLOW}⚠{RESET} {msg}"


def check_file(filepath):
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    errors = []
    warnings = []
    passes = []

    # ─── Dateityp erkennen ────────────────────────────────
    typ = None
    m = re.search(r'DE_A1_\d{4}([VXGRSWC])', filename)
    if m:
        typ = m.group(1)

    print(f"\n{BOLD}{'═'*60}{RESET}")
    print(f"{BOLD}Datei:{RESET} {filename}  (Typ: {typ or '?'})")
    print(f"{'═'*60}")

    # ═══════════════════════════════════════════════════════
    # 1. LAYOUT (daf-html-layout Skill)
    # ═══════════════════════════════════════════════════════
    print(f"\n{BOLD}[1] Layout (daf-html-layout){RESET}")

    # Body: lila Verlauf
    if re.search(r'background:\s*linear-gradient\(135deg,\s*#667eea\s+0%,\s*#764ba2\s+100%\)', content):
        passes.append(ok("Body: lila Verlauf (linear-gradient) korrekt"))
    else:
        errors.append(fail("Body: lila Verlauf FEHLT oder falsch"))

    # Header: padding 30px
    if re.search(r'\.header\s*\{[^}]*padding:\s*30px', content):
        passes.append(ok("Header: padding: 30px"))
    else:
        errors.append(fail("Header: padding: 30px FEHLT"))

    # Header: text-align center
    if re.search(r'\.header\s*\{[^}]*text-align:\s*center', content):
        passes.append(ok("Header: text-align: center"))
    else:
        errors.append(fail("Header: text-align: center FEHLT"))

    # Header: Georgia font
    if re.search(r'Georgia.*serif', content):
        passes.append(ok("Header: Georgia Font für Titel/Untertitel"))
    else:
        errors.append(fail("Header: Georgia Font FEHLT"))

    # Header: big-emoji
    if '.big-emoji' in content or 'big-emoji' in content:
        passes.append(ok("Header: .big-emoji Klasse vorhanden"))
    else:
        errors.append(fail("Header: .big-emoji Klasse FEHLT"))

    # Container: max-width 1000px
    if re.search(r'max-width:\s*1000px', content):
        passes.append(ok("Container: max-width: 1000px"))
    else:
        errors.append(fail("Container: max-width: 1000px FEHLT"))

    # Container: border-radius 12px
    if re.search(r'border-radius:\s*12px', content):
        passes.append(ok("Container: border-radius: 12px"))
    else:
        errors.append(fail("Container: border-radius: 12px FEHLT"))

    # Container: overflow hidden
    if 'overflow: hidden' in content or 'overflow:hidden' in content:
        passes.append(ok("Container: overflow: hidden"))
    else:
        errors.append(fail("Container: overflow: hidden FEHLT"))

    # Container: box-shadow
    if re.search(r'box-shadow:\s*0\s+10px\s+40px\s+rgba\(0,\s*0,\s*0,\s*0\.2\)', content):
        passes.append(ok("Container: box-shadow (0 10px 40px rgba(0,0,0,0.2))"))
    else:
        errors.append(fail("Container: box-shadow FEHLT oder falsch"))

    # Nav: flex-wrap nowrap
    if re.search(r'\.nav\s*\{[^}]*flex-wrap:\s*nowrap', content):
        passes.append(ok("Nav: flex-wrap: nowrap"))
    else:
        errors.append(fail("Nav: flex-wrap: nowrap FEHLT"))

    # Nav: border-top/left/right
    nav_borders = (
        re.search(r'\.nav\s*\{[^}]*border-top:\s*1px\s+solid\s+#ddd', content) and
        re.search(r'\.nav\s*\{[^}]*border-left:\s*1px\s+solid\s+#ddd', content) and
        re.search(r'\.nav\s*\{[^}]*border-right:\s*1px\s+solid\s+#ddd', content)
    )
    if nav_borders:
        passes.append(ok("Nav: border-top, border-left, border-right"))
    else:
        errors.append(fail("Nav: border-top/left/right FEHLT"))

    # Nav-btn: border-right und border-bottom
    if (re.search(r'\.nav-btn\s*\{[^}]*border-right:\s*1px\s+solid\s+#ddd', content) and
        re.search(r'\.nav-btn\s*\{[^}]*border-bottom:\s*1px\s+solid\s+#ddd', content)):
        passes.append(ok("Nav-btn: border-right, border-bottom"))
    else:
        errors.append(fail("Nav-btn: border-right/border-bottom FEHLT"))

    # Nav-btn: display flex, flex-direction column
    if (re.search(r'\.nav-btn\s*\{[^}]*display:\s*flex', content) and
        re.search(r'\.nav-btn\s*\{[^}]*flex-direction:\s*column', content)):
        passes.append(ok("Nav-btn: display: flex; flex-direction: column"))
    else:
        errors.append(fail("Nav-btn: flex-direction column FEHLT"))

    # Nav-btn: KEIN border: none nach border-right
    if re.search(r'\.nav-btn\s*\{[^}]*border-right:[^}]*?border:\s*none', content):
        errors.append(fail("Nav-btn: border: none nach border-right (VERBOTEN)"))
    else:
        passes.append(ok("Nav-btn: KEIN 'border: none' nach border-right"))

    # Mobile responsive: @media (max-width: 600px)
    if re.search(r'@media\s*\(\s*max-width:\s*600px\s*\)', content):
        passes.append(ok("Mobile Responsive: @media (max-width: 600px) vorhanden"))
    else:
        errors.append(fail("Mobile Responsive: @media Query FEHLT"))

    # ═══════════════════════════════════════════════════════
    # 2. TIMER / BUTTONS (timer-bar, btn-row)
    # ═══════════════════════════════════════════════════════
    print(f"\n{BOLD}[2] Timer & Buttons{RESET}")

    # Timer-bar (nicht control-bar!)
    if '.timer-bar' in content:
        passes.append(ok("Timer-bar: .timer-bar CSS Klasse vorhanden"))
    else:
        errors.append(fail("Timer-bar: .timer-bar FEHLT (alte .control-bar verwenden?)"))

    # Timer-bar weiß und Schatten
    if (re.search(r'\.timer-bar\s*\{[^}]*background:\s*white', content) and
        re.search(r'\.timer-bar\s*\{[^}]*box-shadow', content)):
        passes.append(ok("Timer-bar: white background + box-shadow"))
    else:
        errors.append(fail("Timer-bar: white background oder box-shadow FEHLT"))

    # Timer-IDs: timer-N (nicht tN)
    timer_ids = re.findall(r'id="(?:timer-|best-)\d+"', content)
    if timer_ids:
        passes.append(ok(f"Timer-IDs: Gefunden {len(timer_ids)} Timer-IDs (timer-N, best-N Format)"))
    else:
        warnings.append(warn("Timer-IDs: Keine Timer-IDs gefunden (optional für manche Tabs)"))

    # Btn-row mit Buttons
    if '.btn-row' in content:
        passes.append(ok("Btn-row: .btn-row CSS Klasse vorhanden"))
    else:
        warnings.append(warn("Btn-row: .btn-row Klasse FEHLT (optional)"))

    # Buttons: KEIN lila Hintergrund
    if re.search(r'\.btn\s*\{[^}]*background:\s*none', content):
        passes.append(ok("Btn: background: none (kein farbiger Hintergrund)"))
    else:
        errors.append(fail("Btn: background sollte 'none' sein (nicht lila/gradient)"))

    # Buttons: border 1px solid #ddd oder #c0b0e8
    if (re.search(r'\.btn\s*\{[^}]*border:\s*1px\s+solid\s+#ddd', content) or
        re.search(r'\.btn\s*\{[^}]*border:\s*1px\s+solid\s+#c0b0e8', content)):
        passes.append(ok("Btn: border: 1px solid (#ddd oder #c0b0e8)"))
    else:
        errors.append(fail("Btn: border style FEHLT oder falsch"))

    # VERBOTEN: .control-bar (veraltet)
    if re.search(r'class="control-bar"', content) or re.search(r'\.control-bar\s*\{', content):
        errors.append(fail("VERBOTEN: .control-bar gefunden — korrekt: .timer-bar (weiß, Schatten) + .btn-row"))
    else:
        passes.append(ok("Kein .control-bar (veraltetes Pattern)"))

    # VERBOTEN: score-box / Richtig-Anzeige in timer-bar
    timer_bar_blocks = re.findall(r'<div class="timer-bar"[^>]*>.*?</div>\s*</div>', content, re.DOTALL)
    richtig_in_timer = any('Richtig:' in b or 'score-box' in b for b in timer_bar_blocks)
    if richtig_in_timer:
        errors.append(fail("VERBOTEN: 'Richtig:'/score-box in timer-bar — Timer-Bar enthält NUR Timer + Bestzeit"))
    else:
        passes.append(ok("Keine Richtig/Score-Anzeige in timer-bar"))

    # Lösungen-Button wenn Neu-Button vorhanden
    has_neu_btn = re.search(r'↺\s*Neu|&#8634;.*Neu|Neu.*↺', content) or 'onclick.*Reset' in content
    has_loesung_btn = 'Lösungen' in content or 'L&ouml;sungen' in content or '💡' in content
    if has_neu_btn and not has_loesung_btn:
        errors.append(fail("Neu-Button vorhanden aber KEIN Lösungen-Button — Skill: immer beide Buttons"))
    elif has_loesung_btn:
        passes.append(ok("Neu + Lösungen-Buttons vorhanden"))

    # Ungesicherte score/total DOM-Zugriffe
    unguarded = re.findall(r"document\.getElementById\('(?:score|total)\d+'\)\.textContent", content)
    if unguarded:
        errors.append(fail(f"Ungesicherter score/total DOM-Zugriff ({len(unguarded)}x) — immer mit if(el) absichern"))
    else:
        passes.append(ok("DOM-Zugriffe auf score/total abgesichert"))

    # ═══════════════════════════════════════════════════════
    # 3. SATZBAU (satzbau-drag-drop) — nur wenn vorhanden
    # ═══════════════════════════════════════════════════════
    print(f"\n{BOLD}[3] Satzbau (satzbau-drag-drop){RESET}")

    has_satzbau = 'satzbauData' in content or 'satzbauContainer' in content
    if has_satzbau:
        passes.append(ok("Satzbau-Tab: satzbauData oder satzbauContainer vorhanden"))

        # satzbauData mit parts, valid, punct
        if re.search(r'var\s+satzbauData\s*=\s*\[', content):
            passes.append(ok("satzbauData: Variable deklariert"))
        else:
            errors.append(fail("satzbauData: Variable FEHLT"))

        # Chips: white background + #667eea border
        if (re.search(r'\.chip\s*\{[^}]*background:\s*white', content) and
            re.search(r'\.chip\s*\{[^}]*border:[^}]*#667eea', content)):
            passes.append(ok("Satzbau-Chips: white background + #667eea border"))
        else:
            errors.append(fail("Satzbau-Chips: white bg oder #667eea border FEHLT"))

        # KEIN "Satz 1/2/3"-Label
        if re.search(r"textContent\s*=\s*['\"]Satz\s+\d+['\"]", content):
            errors.append(fail("Satzbau: 'Satz 1/2/3'-Label vorhanden (VERBOTEN)"))
        else:
            passes.append(ok("Satzbau: KEIN 'Satz 1/2/3'-Label"))

        # initSatzbau() Funktion
        if 'function initSatzbau' in content:
            passes.append(ok("initSatzbau(): Funktion vorhanden"))
        else:
            errors.append(fail("initSatzbau(): Funktion FEHLT"))

        # sbDragged, sbMakeChip, etc.
        sb_funcs = ['sbDragged', 'sbMakeChip', 'sbRegisterZone', 'sbColorRow', 'sbCheckAuto', 'sbShowSolution']
        found_funcs = sum(1 for f in sb_funcs if f in content)
        if found_funcs >= 5:
            passes.append(ok(f"Satzbau-Funktionen: {found_funcs}/{len(sb_funcs)} vorhanden"))
        else:
            errors.append(fail(f"Satzbau-Funktionen: nur {found_funcs}/{len(sb_funcs)} vorhanden"))

        # timerAutoStart beim ersten Drag
        if re.search(r'dragstart.*timerAutoStart', content) or 'dragstart' in content and 'timerAutoStart' in content:
            passes.append(ok("Satzbau: timerAutoStart bei Drag-Start"))
        else:
            warnings.append(warn("Satzbau: timerAutoStart nicht beim dragstart erkannt"))
    else:
        passes.append(ok("Satzbau-Tab: nicht vorhanden (optional)"))

    # ═══════════════════════════════════════════════════════
    # 4. ÜBUNGSFORMEN (daf-uebungsformen)
    # ═══════════════════════════════════════════════════════
    print(f"\n{BOLD}[4] Übungsformen (daf-uebungsformen){RESET}")

    # KEIN Prüfen-Button
    if (re.search(r'Prüfen|Lösungen prüfen|Check', content, re.IGNORECASE) and
        re.search(r'button.*Prüfen', content, re.IGNORECASE)):
        errors.append(fail("Prüfen-Button: vorhanden (VERBOTEN - live feedback verwenden)"))
    else:
        passes.append(ok("KEIN Prüfen-Button"))

    # liveCheck() für case-sensitive Vergleich
    if 'function liveCheck' in content:
        # Check for case-sensitivity logic
        if 'case' in content.lower() or 'toLowerCase' in content:
            passes.append(ok("liveCheck(): Funktion vorhanden"))
        else:
            warnings.append(warn("liveCheck(): Funktion vorhanden, aber case-sensitivity unklar"))
    else:
        warnings.append(warn("liveCheck(): Funktion nicht gefunden (optional)"))

    # wortschatzCheck() für Wortschatz-Tab
    if 'wortschatzCheck' in content:
        passes.append(ok("wortschatzCheck(): Funktion vorhanden"))
    else:
        warnings.append(warn("wortschatzCheck(): Nicht vorhanden (nur wenn Wortschatz-Tab)"))

    # .ok / .no CSS für Lückentext
    if ('.ok' in content and '.no' in content):
        passes.append(ok("Lückentext: .ok / .no CSS vorhanden"))
    else:
        warnings.append(warn("Lückentext: .ok / .no CSS unklar"))

    # ═══════════════════════════════════════════════════════
    # 5. WORTSCHATZ-TAB (falls vorhanden)
    # ═══════════════════════════════════════════════════════
    print(f"\n{BOLD}[5] Wortschatz-Tab{RESET}")

    has_wortschatz = 'WORTSCHATZ' in content or 'wortschatzContainer' in content
    if has_wortschatz:
        passes.append(ok("Wortschatz-Tab: WORTSCHATZ oder wortschatzContainer vorhanden"))

        # .luecken-item + input.blank CSS
        if ('.luecken-item' in content and 'input.blank' in content):
            passes.append(ok("Wortschatz-Karten: .luecken-item + input.blank vorhanden"))
        else:
            errors.append(fail("Wortschatz-Karten: .luecken-item oder input.blank FEHLT"))

        # type: "p" (nicht "v"/"a")
        if re.search(r'type:\s*["\']p["\']', content):
            passes.append(ok("Wortschatz: type:'p' für Adjektive/Verben vorhanden"))
        else:
            warnings.append(warn("Wortschatz: type:'p' nicht erkannt"))

        # 2-Spalten-Grid
        if re.search(r'grid-template-columns:\s*1fr\s+1fr', content) or 'grid-template-columns: 1fr 1fr' in content:
            passes.append(ok("Wortschatz: 2-Spalten-Grid vorhanden"))
        else:
            warnings.append(warn("Wortschatz: 2-Spalten-Grid nicht erkannt"))

        # initWortschatz(), showWortschatzLoesung(), resetWortschatz(), checkWortschatzAllOk()
        ws_funcs = ['initWortschatz', 'showWortschatzLoesung', 'resetWortschatz', 'checkWortschatzAllOk']
        found_ws = sum(1 for f in ws_funcs if f in content)
        if found_ws >= 3:
            passes.append(ok(f"Wortschatz-Funktionen: {found_ws}/{len(ws_funcs)} vorhanden"))
        else:
            warnings.append(warn(f"Wortschatz-Funktionen: nur {found_ws}/{len(ws_funcs)}"))

        # Emojis im en-Feld (optional aber empfohlen)
        if re.search(r'en:\s*["\'][😀-🙏🌀-🗿]', content):
            passes.append(ok("Wortschatz: Emojis im en-Feld (optional)"))
        else:
            warnings.append(warn("Wortschatz: Emojis im en-Feld nicht erkannt"))

        # KEIN liveCheck() im Wortschatz-Tab
        if re.search(r'\.blank.*liveCheck', content):
            errors.append(fail("Wortschatz: liveCheck() verwenden (VERBOTEN - wortschatzCheck() statt dessen)"))
        else:
            passes.append(ok("Wortschatz: wortschatzCheck() wird verwendet, nicht liveCheck()"))
    else:
        passes.append(ok("Wortschatz-Tab: nicht vorhanden (optional)"))

    # ═══════════════════════════════════════════════════════
    # 6. BILDER-PFLICHT (daf-bilder-pflicht)
    # ═══════════════════════════════════════════════════════
    print(f"\n{BOLD}[6] Bilder-Pflicht (daf-bilder-pflicht){RESET}")

    # Tab-Banner CSS
    if '.tab-banner' in content:
        passes.append(ok("Tab-Banner: .tab-banner CSS vorhanden"))
    else:
        warnings.append(warn("Tab-Banner: .tab-banner CSS FEHLT"))

    # Mindestanzahl Banners je nach Typ
    section_count = len(re.findall(r'class="section"', content))
    banner_count = len(re.findall(r'class="tab-banner"', content))
    if banner_count > 0:
        passes.append(ok(f"Tab-Banner: {banner_count} Bilder vorhanden ({section_count} Tabs)"))
        if banner_count < section_count:
            warnings.append(warn(f"Tab-Banner: {section_count - banner_count} Banner fehlen"))
    else:
        errors.append(fail("Tab-Banner: KEINE Banners vorhanden (Pflicht!)"))

    # ═══════════════════════════════════════════════════════
    # 7. SONSTIGES
    # ═══════════════════════════════════════════════════════
    print(f"\n{BOLD}[7] Sonstiges{RESET}")

    # Kein startsWith-Fehler
    if re.search(r'\.startsWith\s*\(', content):
        warnings.append(warn("startsWith() verwendet (prüfe auf Präfix-Logik-Bug)"))
    else:
        passes.append(ok("KEIN startsWith() Pattern"))

    # DOM-Zugriffe auf score/total mit if(el) absichert
    if re.search(r"getElementById.*score|getElementById.*total", content):
        if re.search(r"if\s*\(\s*el\s*\)", content) or re.search(r"document\.getElementById[^;]*\.", content):
            passes.append(ok("Score/Total DOM-Zugriffe mit Checks"))
        else:
            warnings.append(warn("Score/Total DOM-Zugriffe - sollten mit if(el) absichert sein"))

    # section.active (nicht section.aktiv)
    if 'section.active' in content or "classList.add('active')" in content:
        passes.append(ok("Section-Klasse: .active (korrekt)"))
    else:
        errors.append(fail("Section-Klasse: .active nicht korrekt implementiert"))

    # Doppelter Footer
    footer_count = len(re.findall(r'class="author-footer"', content))
    if footer_count == 1:
        passes.append(ok("Footer: genau 1 Footer vorhanden"))
    elif footer_count > 1:
        errors.append(fail(f"Footer: {footer_count} Footer vorhanden (nur 1 erlaubt)"))
    else:
        errors.append(fail("Footer: KEIN Footer vorhanden"))

    # Kein .footer CSS
    if re.search(r'\.footer\s*\{', content):
        errors.append(fail("CSS: .footer Klasse vorhanden (sollte .author-footer sein)"))
    else:
        passes.append(ok("CSS: KEIN .footer (nur .author-footer)"))

    # Footer muss .max-width 1000px haben
    if re.search(r'\.author-footer\s*\{[^}]*max-width:\s*1000px', content):
        passes.append(ok("Footer: max-width: 1000px"))
    else:
        warnings.append(warn("Footer: max-width: 1000px sollte vorhanden sein"))

    # ═══════════════════════════════════════════════════════
    # ZUSAMMENFASSUNG
    # ═══════════════════════════════════════════════════════
    print(f"\n{BOLD}{'═'*60}{RESET}")
    print(f"{BOLD}Zusammenfassung:{RESET}")
    print(f"{'═'*60}")

    for p in passes:
        print(p)

    if warnings:
        for w in warnings:
            print(w)

    if errors:
        for e in errors:
            print(e)

    print(f"\n{BOLD}Ergebnis:{RESET}")
    if errors:
        print(f"{RED}✗ {len(errors)} Fehler{RESET}, {len(warnings)} Warnungen, {len(passes)} OK")
        return False
    else:
        print(f"{GREEN}✓ Alles OK!{RESET} ({len(passes)} Checks bestanden, {len(warnings)} Warnungen)")
        return True


# ─────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────
if __name__ == '__main__':
    if len(sys.argv) < 2:
        # Default: alle DE_A1_*.html im Verzeichnis
        files = sorted(glob.glob('DE_A1_*.html'))
        if not files:
            print(f"{RED}Fehler: Keine DE_A1_*.html Dateien gefunden.{RESET}")
            print(f"Verwendung: python3 check-a11-quality.py [DATEI.html]")
            sys.exit(1)
    else:
        files = sys.argv[1:]

    all_ok = True
    for filepath in files:
        if not os.path.isfile(filepath):
            print(f"{RED}✗ Datei nicht gefunden: {filepath}{RESET}")
            all_ok = False
            continue
        if not check_file(filepath):
            all_ok = False

    print(f"\n{BOLD}{'═'*60}{RESET}")
    if all_ok:
        print(f"{GREEN}✓✓✓ ALLE DATEIEN OK ✓✓✓{RESET}")
        sys.exit(0)
    else:
        print(f"{RED}✗✗✗ FEHLER GEFUNDEN ✗✗✗{RESET}")
        sys.exit(1)
