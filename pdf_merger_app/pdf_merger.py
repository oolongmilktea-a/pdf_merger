import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

try:
    from pypdf import PdfWriter, PdfReader
except ImportError:
    raise SystemExit("Missing dependency: pypdf. Install it with: pip install pypdf")


def merge_pdfs(pdf1_path: str, pdf2_path: str, output_path: str) -> None:
    writer = PdfWriter()
    for path in (pdf1_path, pdf2_path):
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)
    with open(output_path, "wb") as f:
        writer.write(f)


class PDFMergerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("520x240")
        self.pdf1 = tk.StringVar()
        self.pdf2 = tk.StringVar()
        self.output = tk.StringVar(value="merged.pdf")
        self.build_ui()

    def build_ui(self):
        pad = {"padx": 10, "pady": 8}

        tk.Label(self.root, text="PDF 1:").grid(row=0, column=0, sticky="w", **pad)
        tk.Entry(self.root, textvariable=self.pdf1, width=48).grid(row=0, column=1, **pad)
        tk.Button(self.root, text="Browse", command=self.pick_pdf1).grid(row=0, column=2, **pad)

        tk.Label(self.root, text="PDF 2:").grid(row=1, column=0, sticky="w", **pad)
        tk.Entry(self.root, textvariable=self.pdf2, width=48).grid(row=1, column=1, **pad)
        tk.Button(self.root, text="Browse", command=self.pick_pdf2).grid(row=1, column=2, **pad)

        tk.Label(self.root, text="Output file name:").grid(row=2, column=0, sticky="w", **pad)
        tk.Entry(self.root, textvariable=self.output, width=48).grid(row=2, column=1, **pad)

        tk.Button(self.root, text="Merge PDFs", command=self.run_merge, width=20).grid(row=3, column=1, pady=20)

        help_text = (
            "1) Choose two PDF files\n"
            "2) Enter the output file name\n"
            "3) Click Merge PDFs and choose where to save"
        )
        tk.Label(self.root, text=help_text, justify="left").grid(row=4, column=0, columnspan=3, padx=10, sticky="w")

    def pick_pdf1(self):
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path:
            self.pdf1.set(path)

    def pick_pdf2(self):
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path:
            self.pdf2.set(path)

    def run_merge(self):
        pdf1 = self.pdf1.get().strip()
        pdf2 = self.pdf2.get().strip()
        output_name = self.output.get().strip() or "merged.pdf"

        if not pdf1 or not pdf2:
            messagebox.showerror("Missing file", "Please select both PDF files.")
            return

        if not Path(pdf1).exists() or not Path(pdf2).exists():
            messagebox.showerror("File not found", "One or both selected PDF files do not exist.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=output_name,
            filetypes=[("PDF files", "*.pdf")],
        )
        if not save_path:
            return

        try:
            merge_pdfs(pdf1, pdf2, save_path)
            messagebox.showinfo("Success", f"Merged PDF saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not merge PDFs:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
