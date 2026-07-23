# habit_tracker.spec
# Build with: pyinstaller habit_tracker.spec --noconfirm
#
# This bundles app.py + run_app.py + streamlit's static/runtime files
# into a single-folder distributable .exe for Windows.
#
# ROOT-CAUSE FIX (read this if you ever hit build errors again):
# PyInstaller can end up with the SAME binary (e.g. numpy's DLL) added
# twice under two different internal paths when collect_all() pulls in
# a package's own copy of a dependency that PyInstaller's own import
# scanner *also* finds independently (e.g. via pandas). Two copies of
# the same native extension loaded in one process causes:
#   "ImportError: ... numpy: cannot load module more than once per process"
# We fix this at the SOURCE here by de-duplicating a.binaries by
# destination filename right after Analysis, instead of avoiding
# collect_all() (which is what caused the separate
# "No package metadata was found for streamlit" error last time).
# This way we get full metadata + data + binaries from collect_all,
# AND no duplicate-binary crash.

from PyInstaller.utils.hooks import collect_all

block_cipher = None

streamlit_datas, streamlit_binaries, streamlit_hiddenimports = collect_all("streamlit")
pandas_datas, pandas_binaries, pandas_hiddenimports = collect_all("pandas")

a = Analysis(
    ['run_app.py'],
    pathex=[],
    binaries=streamlit_binaries + pandas_binaries,
    datas=streamlit_datas + pandas_datas + [
        ('app.py', '.'),
        ('.streamlit', '.streamlit'),
    ],
    hiddenimports=list(set(
        streamlit_hiddenimports + pandas_hiddenimports + [
            'streamlit.web.cli',
            'streamlit.runtime.scriptrunner.magic_funcs',
            'numpy',
            'matplotlib',
            'matplotlib.backends.backend_agg',
        ]
    )),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# --- THE ACTUAL FIX: de-duplicate binaries by destination filename ---
# Without this, the same numpy/.dll or .pyd can appear twice (once via
# streamlit's deps, once via pandas's deps) under slightly different
# source paths, and PyInstaller's own TOC dedup (which keys on path,
# not just name) won't catch it. Keeping only the first occurrence of
# each destination filename prevents numpy from being loaded twice.
seen_names = set()
deduped_binaries = []
for entry in a.binaries:
    dest_name = entry[0]
    if dest_name not in seen_names:
        seen_names.add(dest_name)
        deduped_binaries.append(entry)
a.binaries = deduped_binaries

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='HabitTracker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,   # set True if you want a console window for debugging
    icon=None,       # put a path to a .ico file here if you have one
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='HabitTracker',
)
