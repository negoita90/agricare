#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("kernel")

# Touchscreen DMI quirk
p = root / "drivers/platform/x86/touchscreen_dmi.c"
s = p.read_text()
anchor = '''	{
		/* Chuwi Hi10 Pro (CWI529) */
		.driver_data = (void *)&chuwi_hi10_pro_data,
		.matches = {
			DMI_MATCH(DMI_BOARD_VENDOR, "Hampoo"),
			DMI_MATCH(DMI_PRODUCT_NAME, "Hi10 pro tablet"),
			DMI_MATCH(DMI_BOARD_NAME, "Cherry Trail CR"),
		},
	},
'''
extra = '''	{
		/* Chuwi Hi10 Pro (CWI529) - alternate Hampoo DMI strings */
		.driver_data = (void *)&chuwi_hi10_pro_data,
		.matches = {
			DMI_MATCH(DMI_SYS_VENDOR, "Hampoo"),
			DMI_MATCH(DMI_PRODUCT_NAME, "I1D6_C109S_Hi10Pro"),
			DMI_MATCH(DMI_BOARD_VENDOR, "Hampoo"),
			DMI_MATCH(DMI_BOARD_NAME, "Cherry Trail CR"),
		},
	},
'''
if "I1D6_C109S_Hi10Pro" not in s:
    if anchor not in s:
        raise SystemExit("Touchscreen Hi10 Pro DMI anchor not found")
    s = s.replace(anchor, anchor + extra, 1)
    p.write_text(s)

# Panel orientation quirk
p = root / "drivers/gpu/drm/drm_panel_orientation_quirks.c"
s = p.read_text()
anchor = '''	}, {	/* Chuwi Hi10 Pro (CWI529) */
		.matches = {
		  DMI_EXACT_MATCH(DMI_BOARD_VENDOR, "Hampoo"),
		  DMI_EXACT_MATCH(DMI_PRODUCT_NAME, "Hi10 pro tablet"),
		},
		.driver_data = (void *)&lcd1200x1920_rightside_up,
'''
extra = '''	}, {	/* Chuwi Hi10 Pro (CWI529) - alternate Hampoo DMI strings */
		.matches = {
		  DMI_EXACT_MATCH(DMI_SYS_VENDOR, "Hampoo"),
		  DMI_EXACT_MATCH(DMI_PRODUCT_NAME, "I1D6_C109S_Hi10Pro"),
		  DMI_EXACT_MATCH(DMI_BOARD_NAME, "Cherry Trail CR"),
		},
		.driver_data = (void *)&lcd1200x1920_rightside_up,
'''
if "I1D6_C109S_Hi10Pro" not in s:
    if anchor not in s:
        raise SystemExit("Panel orientation Hi10 Pro DMI anchor not found")
    s = s.replace(anchor, anchor + extra, 1)
    p.write_text(s)

print("Patch applied successfully")
