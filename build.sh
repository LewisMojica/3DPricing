rm -r build dist;
pyinstaller entry.py;
cp createTables.sqlite.sql dist/entry/;
cp imgs/icons/main_icon.png dist/entry/;
cp config.json dist/entry;
cp LICENSE dist/entry;
mv dist/entry/entry dist/entry/3DPricing;
mv dist/entry dist/3DPricing;
