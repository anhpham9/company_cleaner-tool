# 👨‍💻 開発者向け / Dành cho Developer

## ⚙️ ビルド方法 / Build

```bash
pip install pyinstaller customtkinter tkinterdnd2 pandas openpyxl requests

pyinstaller --onefile --noconsole --clean --icon=assets/icon.ico main.py --version-file version.txt
```

---

## 🔄 バージョン更新 / Update version

### Minor Update（例：1.1 → 1.2）

```bash
python bump_version.py --note "アイコン変更"

git add .
git commit -m "release 1.2"
git push
```

---

### Major Update（例：2.6 → 3.0）

```bash
python bump_version.py --major --note "大幅アップデート"

git add .
git commit -m "release 3.0"
git push
```

---

### version のみ更新（noteなし）

```bash
python bump_version.py

git add .
git commit -m "release x.x"
git push
```

---

## 🚀 GitHub Actions

```txt
→ version.json 更新検知
→ exe ビルド
→ GitHub Release 作成
→ exe アップロード
→ SHA256 / size 生成
→ version.json 更新
→ 自動コミット
```

---

## 📲 自動アップデート処理

```txt
→ version.json チェック
→ 新バージョン検知
→ exe ダウンロード
→ SHA256 検証
→ 自動アップデート
```

---

# 🤝 Contributing

Issues / Pull Requests welcome.

---

# 📄 License

Internal / Private use

---

# 📦 Download

https://github.com/anhpham9/company_cleaner-tool/releases/latest

---

# 📌 今後の予定 / Future Plans

* [ ] ブラックリストUI設定
* [ ] 多言語対応
* [x] 自動アップデート改善
* [ ] ダークモード対応
