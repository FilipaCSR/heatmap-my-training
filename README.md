# Heatmap My Training 📊

Visualize your Apple Health exercise data with heatmaps.
Just upload your `export.xml` or a filtered `.csv` and instantly see your training trends for the year. No code required!

---

## ✨ Features

* 🌍 Streamlit web app – just open and upload
* 🔢 Asthetic heatmap design
* 📊 Multiple years side by side
* 💡 Normalize color scales across years (optional)
* 📂 Export heatmaps as PNG
* ❤️ Easy to use, no technical knowledge needed

---

## 🔄 Try it Live

> [https://your-username.streamlit.app](https://your-username.streamlit.app)
> *(Replace with your real URL after deployment)*

---

## 🔍 Example

![Example heatmap](screenshots/example.png)
*See how your training consistency evolves over the year!*

---

## 🎓 How to Use

1. **Export your Apple Health data** from your iPhone:

   * Open the Health app → Profile → Export All Health Data
   * Save the `.zip`, extract it, and locate the `export.xml`
   * Full guide: [How to extract Apple Health data](https://medium.com/@filipacsr/how-to-extract-and-analyze-apple-health-data-with-r-7d28029d22bd)

2. **Run the app locally**:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Or **upload to Streamlit Cloud** to share it online with a link.

---

## 📁 Project Structure

```
heatmap-my-training/
├── app.py                  # Streamlit interface
├── heatmap_design.py      # Apple-style heatmap plot function
├── convert_xml_to_csv.py  # Optional: convert raw XML to full CSV
├── requirements.txt       # Dependencies
├── README.md              # This file
└── .streamlit/
    └── config.toml     # (Optional) UI settings
```

---

## 🚀 Deployment (optional)

1. Push this repo to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "New App" and select this repo + `app.py`

---

## ☕ Support This Project

If you enjoy it, [Buy Me a Coffee](https://www.buymeacoffee.com/filipacsr) ☕


---

Built with ❤️ by [Filipa](https://medium.com/@filipacsr)
=======
# heatmap-my-training
Visualize your Apple Health exercise data with heatmaps. Just upload your export.xml and get yearly insights - no code needed!
