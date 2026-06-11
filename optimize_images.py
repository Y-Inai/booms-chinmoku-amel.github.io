#!/usr/bin/env python3
"""images/ フォルダ内の画像を一括圧縮するスクリプト。
使い方: pip install Pillow → python3 optimize_images.py
元画像は images_backup/ に退避され、同じファイル名で圧縮版に置き換わります（HTMLの修正は不要）。"""
import shutil
from pathlib import Path
from PIL import Image

SRC = Path("images")
BAK = Path("images_backup")
MAX_W = 1600      # 最大幅(px)。これ以上は縮小
QUALITY = 80      # JPEG品質

BAK.mkdir(exist_ok=True)
total_before = total_after = 0
for p in sorted(SRC.iterdir()):
    if p.suffix.lower() not in (".jpg", ".jpeg", ".png"):
        continue
    before = p.stat().st_size
    shutil.copy2(p, BAK / p.name)          # バックアップ
    img = Image.open(p)
    if img.width > MAX_W:
        img = img.resize((MAX_W, int(img.height * MAX_W / img.width)), Image.LANCZOS)
    if p.suffix.lower() == ".png":
        img.save(p, optimize=True)
    else:
        img = img.convert("RGB")
        img.save(p, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    after = p.stat().st_size
    total_before += before; total_after += after
    print(f"{p.name}: {before//1024}KB → {after//1024}KB")
print(f"\n合計: {total_before//1024}KB → {total_after//1024}KB（{100 - total_after*100//max(total_before,1)}%削減）")
