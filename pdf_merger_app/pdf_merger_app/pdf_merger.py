import os
import tkinter as tk
from tkinter import filedialog, messagebox

try:
    from pypdf import PdfReader, PdfWriter
except ImportError as exc:
    raise SystemExit(
        "Missing dependency: pypdf\n"
        "Install it with: pip install pypdf"
    ) from exc


class PDFMergerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("560x260")
        self.root.resizable(False, False)

        self.pdf1_path = tk.StringVar()
        self.pdf2_path = tk.StringVar()
        self.output_path = tk.StringVar()

        self._build_ui()

    def _build_ui(self) -> None:
        padding = {"padx": 10, "pady": 8}

        title = tk.Label(
            self.root,
            text="Merge Two PDFs",
            font=("Arial", 16, "bold")
        )
        title.grid(row=0, column=0, columnspan=3, **padding)

        tk.Label(self.root, text="First PDF:").grid(row=1, column=0, sticky="e", **padding)
        tk.Entry(self.root, textvariable=self.pdf1_path, width=48).grid(row=1, column=1, **padding)
        tk.Button(self.root, text="Browse", command=self.select_pdf1).grid(row=1, column=2, **padding)

        tk.Label(self.root, text="Second PDF:").grid(row=2, column=0, sticky="e", **padding)
        tk.Entry(self.root, textvariable=self.pdf2_path, width=48).grid(row=2, column=1, **padding)
        tk.Button(self.root, text="Browse", command=self.select_pdf2).grid(row=2, column=2, **padding)

        tk.Label(self.root, text="Save As:").grid(row=3, column=0, sticky="e", **padding)
        tk.Entry(self.root, textvariable=self.output_path, width=48).grid(row=3, column=1, **padding)
        tk.Button(self.root, text="Browse", command=self.select_output).grid(row=3, column=2, **padding)

        tk.Button(
            self.root,
            text="Merge PDFs",
            command=self.merge_pdfs,
            width=20,
            height=2
        ).grid(row=4, column=0, columnspan=3, pady=20)

        instructions = tk.Label(
            self.root,
            text="Select two PDF files, choose an output filename, then click Merge PDFs.",
            fg="gray"
        )
        instructions.grid(row=5, column=0, columnspan=3, padx=10, pady=5)

    def select_pdf1(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path:
            self.pdf1_path.set(path)
            self._suggest_output()

    def select_pdf2(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path:
            self.pdf2_path.set(path)
            self._suggest_output()

    def select_output(self) -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile="merged.pdf"
        )
        if path:
            self.output_path.set(path)

    def _suggest_output(self) -> None:
        pdf1 = self.pdf1_path.get()
        pdf2 = self.pdf2_path.get()
        if pdf1 and pdf2 and not self.output_path.get():
            base1 = os.path.splitext(os.path.basename(pdf1))[0]
            base2 = os.path.splitext(os.path.basename(pdf2))[0]
            suggested = f"{base1}_{base2}_merged.pdf"
            self.output_path.set(os.path.join(os.path.dirname(pdf1), suggested))

    def merge_pdfs(self) -> None:
        pdf1 = self.pdf1_path.get().strip()
        pdf2 = self.pdf2_path.get().strip()
        output = self.output_path.get().strip()

        if not pdf1 or not pdf2 or not output:
            messagebox.showerror("Missing information", "Please select both PDFs and an output file.")
            return

        if not os.path.isfile(pdf1) or not os.path.isfile(pdf2):
            messagebox.showerror("File not found", "One or both selected PDF files do not exist.")
            return

        try:
            writer = PdfWriter()

            for path in (pdf1, pdf2):
                reader = PdfReader(path)
                for page in reader.pages:
                    writer.add_page(page)

            with open(output, "wb") as f:
                writer.write(f)

            messagebox.showinfo("Success", f"Merged PDF saved to:\n{output}")
        except Exception as exc:
            messagebox.showerror("Error", f"Could not merge PDFs:\n{exc}")


def main() -> None:
    root = tk.Tk()
    PDFMergerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
