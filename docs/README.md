# 企業リストクリーナー (Company Cleaner)

Excelの企業リストを整理・クリーニングする社内向けツールです。  
Đây là công cụ nội bộ dùng để làm sạch và xử lý danh sách công ty trong Excel.

---

## 📸 Demo

![CompanyCleaner](docs/assets/ui.png)

---

# 📌 主な機能 / Tính năng chính

本ツールでは、以下の処理を自動で実行します。  
Công cụ tự động thực hiện các chức năng sau.

---

## ✅ 会社名の正規化 / Chuẩn hóa tên công ty

- `/xxxx` の削除  
  → Xóa phần `/xxxx`

- 全角 → 半角変換（ＡＢＣ → ABC）  
  → Chuyển ký tự full-width sang half-width

- 不要なスペース削除  
  → Xóa khoảng trắng dư

---

## ✅ 重複企業の削除 / Xóa công ty trùng lặp

- 会社名ベースで重複を判定  
  → Xóa dữ liệu trùng dựa trên tên công ty

---

## ✅ ブラックリストチェック / Kiểm tra blacklist

- blacklist.xlsx と照合して除外  
  → So sánh với file blacklist và loại bỏ khỏi danh sách

- 過去に対応不要と判断された企業を自動除外  
  → Tự động loại bỏ những công ty không cần xử lý

---

## ✅ Excelフォーマット維持 / Giữ nguyên định dạng Excel

以下の情報を保持します。  
Giữ nguyên các định dạng của file Excel.

- 列幅 / Độ rộng cột
- 色 / Màu sắc
- レイアウト / Layout

---

## ✅ ログ出力 / Xuất log

削除されたデータを理由付きで出力します。  
Xuất danh sách dữ liệu bị xóa kèm lý do.

---

## ✅ 出力ファイルを直接オープン / Mở trực tiếp file kết quả

処理完了後、表示されたパスをクリックするとExcelファイルを直接開けます。  
Sau khi xử lý xong, có thể click vào đường dẫn để mở trực tiếp file Excel.

---

# 📋 準備 / Chuẩn bị

## 📄 ブラックリスト設定 / Thiết lập blacklist

### 📌 目的 / Mục đích

以下の企業を自動除外するために使用します。  
Dùng để tự động loại bỏ các công ty không cần xử lý.

- 重複アプローチ防止  
  → Tránh liên hệ trùng

- 過去に断られた企業への再連絡防止  
  → Tránh liên hệ lại công ty đã từ chối

- 不要データ削減  
  → Giảm dữ liệu không cần thiết

---

### 📂 配置場所 / Vị trí file

`blacklist.xlsx` を `CompanyCleaner.exe` と同じフォルダに配置してください。  
Đặt file `blacklist.xlsx` cùng thư mục với `CompanyCleaner.exe`.

例：

```txt
CompanyCleaner/
 ├── CompanyCleaner.exe
 ├── blacklist.xlsx
````

---

### 📄 ファイル名 / Tên file

固定ファイル名：

```txt
blacklist.xlsx
```

⚠️ ファイル名が異なる場合、認識されません。

⚠️ Nếu tên file khác, chương trình sẽ không nhận diện được.

---

### 📋 必須列 / Cột bắt buộc

| 列名  |
| --- |
| 会社名 |

例：

| 会社名      |
| -------- |
| 株式会社ABC  |
| 株式会社サンプル |
| ABC株式会社  |

---

### 📌 blacklist.xlsx が存在しない場合

ブラックリストチェックはスキップされます。

Nếu không tồn tại `blacklist.xlsx`, chương trình sẽ bỏ qua bước kiểm tra blacklist.

---

# 🖥️ 使い方 / Cách sử dụng

## 方法①：ドラッグ＆ドロップ / Kéo & thả

1. アプリを起動
   → Mở ứng dụng (.exe)

2. Excelファイルを画面へドラッグ
   → Kéo file Excel vào ứng dụng

3. 自動処理
   → Tự động xử lý

---

## 方法②：ファイル選択 / Chọn file

1. アプリを起動
   → Mở ứng dụng (.exe)

2. 「ファイル選択」をクリック
   → Nhấn nút chọn file

3. Excelファイルを選択
   → Chọn file Excel cần xử lý

4. 自動処理
   → Tự động xử lý

---

# 📋 入力ファイル仕様 / Quy định file đầu vào

## 必須列 / Cột bắt buộc

| 列名  |
| --- |
| 会社名 |

その他の列は自由です。

Những cột khác có thể tùy ý và sẽ được giữ nguyên.

---

# 📂 出力ファイル / File kết quả

元ファイルと同じフォルダに以下のファイルが生成されます。

Các file sau sẽ được tạo trong cùng thư mục với file gốc.

| ファイル             | 内容                      |
| ---------------- | ----------------------- |
| `*_cleaned.xlsx` | 処理済みデータ / File đã xử lý |
| `*_log.xlsx`     | 削除ログ / File log         |

処理完了後、表示されたパスをクリックすると直接ファイルを開けます。

Sau khi xử lý xong, có thể click vào đường dẫn để mở trực tiếp file.

---

# ⚠️ 注意事項 / Lưu ý

* `.xlsx` ファイルのみ対応
  → Chỉ hỗ trợ file `.xlsx`

* 初回起動時にWindows警告が表示される場合があります

  → Có thể xuất hiện cảnh báo Windows khi chạy lần đầu

「詳細情報」→「実行」を選択してください。

Hãy chọn “More info” → “Run anyway”.

![Windowsの警告](docs/assets/warning.png)

![詳細情報](docs/assets/click-detail.png)

---

# 🔄 自動アップデート / Tự động cập nhật

本ツールは自動アップデートに対応しています。
Công cụ hỗ trợ tự động cập nhật phiên bản.

* 最新バージョン確認
  → Kiểm tra phiên bản mới

* 新バージョンダウンロード
  → Tải phiên bản mới

* SHA256ハッシュ検証
  → Kiểm tra hash SHA256 để đảm bảo an toàn

* 自動更新
  → Tự động cập nhật ứng dụng

※ インターネット接続が必要です。

※ Cần có kết nối internet.

---

# 🛠️ 技術情報 / Tech Stack

* Python
* pandas
* openpyxl
* CustomTkinter
* PyInstaller
* tkinterdnd2
* pillow

---

# 👨‍💻 開発者向け / Dành cho Developer

## ⚙️ ビルド方法 / Build

```bash
pip install pyinstaller customtkinter tkinterdnd2 pandas openpyxl requests pillow

pyinstaller --onefile --noconsole --clean ^
  --icon=assets/icon.ico ^
  main.py ^
  --version-file version.txt
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

---

# 📞 サポート / Support

不具合や改善要望があれば連絡してください。

Nếu có lỗi hoặc yêu cầu cải thiện, vui lòng liên hệ.
