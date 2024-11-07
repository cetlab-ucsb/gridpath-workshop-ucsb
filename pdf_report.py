# Save this code as generate_pdf_report.py

import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image
import matplotlib.pyplot as plt
import os
import textwrap

def generate_pdf_report(directory, plot_details_csv, output_pdf_filename, tables=None, add_tables=False):
    """
    Generates a PDF report with plots, titles, paragraphs, and tables.

    Parameters:
    - directory (str): The base directory where images and CSV files are stored.
    - plot_details_csv (str): The filename of the CSV file with plot details.
    - output_pdf_filename (str): The filename for the output PDF.
    - tables (list of pd.DataFrame, optional): List of tables to include in the PDF.
    - add_tables (bool, optional): Whether to add tables to the PDF.

    """

    # Directory where your plot images are stored
    plot_directory = os.path.join(directory, 'plots')

    max_table_rows_per_page = 50
    page_width, page_height = 8.5, 11

    # Load logos
    emlab_logo_path = os.path.join(directory, 'gridpath-workshop-ucsb/images/emlab_logo_horizontal.png')
    cetlab_logo_path = os.path.join(directory, 'gridpath-workshop-ucsb/images/cetlab_logo.png')
    wri_logo_path = os.path.join(directory, 'gridpath-workshop-ucsb/images/WRI-India-logo.png')
    #prayas_logo_path = os.path.join(directory, 'gridpath-workshop-ucsb/images/Prayas_logo.png')

    # Load logos as images
    emlab_logo_image = Image.open(emlab_logo_path)
    cetlab_logo_image = Image.open(cetlab_logo_path)
    wri_logo_image = Image.open(wri_logo_path)
    #prayas_logo_image = Image.open(prayas_logo_path)
        
    def truncate_text(text, max_width):
        if len(text) > max_width:
            return text[:max_width - 3] + '...'
        else:
            return text

    def add_footer_logos(fig, logos):
        logo_x_position = 0.05
        logo_width, logo_height = 0.1, 0.08
        for logo_image in logos:
            ax_logo = fig.add_axes([logo_x_position, 0.02, logo_width, logo_height])
            ax_logo.imshow(logo_image)
            ax_logo.axis('off')
            logo_x_position += 0.12

    def add_plot_with_description(pdf, image_path, title, description, logos):
        title_fontsize = 18
        description_fontsize = 12
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis('off')
        full_width_margin = 0.05
        full_width = 1 - 2 * full_width_margin
        wrapped_title = "\n".join(textwrap.wrap(title, width=70))
        wrapped_description = "\n".join(textwrap.wrap(description, width=100))
        fig.text(0.5, 0.88, wrapped_title, ha='center', fontsize=title_fontsize, weight='bold')
        image = Image.open(image_path)
        ax.imshow(image)
        ax.axis('off')
        ax.set_position([full_width_margin, 0.35, full_width, 0.45])
        fig.text(full_width_margin, 0.25, wrapped_description, ha='left', fontsize=description_fontsize)
        add_footer_logos(fig, logos)
        pdf.savefig(fig)
        plt.close(fig)

    def add_title_page(pdf, title, logos):
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis('off')
        fig.text(0.5, 0.6, title, ha='center', fontsize=28, weight='bold')
        add_footer_logos(fig, logos)
        pdf.savefig(fig)
        plt.close(fig)

    def add_paragraph_page(pdf, title, paragraph_text, logos):
        fig, ax = plt.subplots(figsize=(page_width, page_height))
        ax.axis('off')
        wrapped_text = "\n".join(textwrap.wrap(paragraph_text, width=85))
        fig.text(0.5, 0.9, title, ha='center', fontsize=16, weight='bold')
        fig.text(0.1, 0.8, wrapped_text, ha='left', fontsize=12)
        add_footer_logos(fig, logos)
        pdf.savefig(fig)
        plt.close(fig)

    def add_tables_to_pdf(pdf, tables, logos):
        fig, ax = plt.subplots(figsize=(page_width, page_height))
        ax.axis('off')
        fig.text(0.5, 0.95, "Tables", ha='center', fontsize=16, weight='bold')
        add_footer_logos(fig, logos)
        pdf.savefig(fig)
        plt.close(fig)
        for table_df in tables:
            table_data = table_df.values
            column_labels = table_df.columns
            row_labels = table_df.index
            num_rows = table_data.shape[0]
            for start_row in range(0, num_rows, max_table_rows_per_page):
                end_row = min(start_row + max_table_rows_per_page, num_rows)
                subset_data = table_data[start_row:end_row]
                subset_row_labels = row_labels[start_row:end_row]
                max_cell_width = 8
                for row in range(subset_data.shape[0]):
                    for col in range(subset_data.shape[1]):
                        subset_data[row, col] = truncate_text(str(subset_data[row, col]), max_cell_width)
                fig, ax = plt.subplots(figsize=(page_width, page_height))
                ax.axis('off')
                table = ax.table(cellText=subset_data, colLabels=column_labels, rowLabels=subset_row_labels, loc='center', cellLoc='center')
                table.auto_set_font_size(False)
                table.set_fontsize(10)
                table.scale(1.2, 1.2)
                add_footer_logos(fig, logos)
                pdf.savefig(fig)
                plt.close(fig)

    csv_file_path = os.path.join(directory, plot_details_csv)
    try:
        plot_details = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print(f"Error: The CSV file {csv_file_path} was not found.")
        raise

    content_added = False
    logos = [emlab_logo_image, cetlab_logo_image, wri_logo_image]

    with PdfPages(os.path.join(directory, output_pdf_filename)) as pdf:
        for idx, row in plot_details.iterrows():
            if row['image_filename'] == "report_title":
                add_title_page(pdf, row['plot_title'], logos)
                content_added = True
            elif row['image_filename'] == "para_text":
                add_paragraph_page(pdf, row['plot_title'], row['plot_description'], logos)
            else:
                image_path = os.path.join(plot_directory, row['image_filename'])
                try:
                    title = row['plot_title']
                    description = row['plot_description']
                    if os.path.exists(image_path):
                        add_plot_with_description(pdf, image_path, title, description, logos)
                        content_added = True
                    else:
                        print(f"Warning: Image file {image_path} not found.")
                except KeyError as e:
                    print(f"KeyError: Column {e} not found in the CSV.")
                    raise
        if add_tables and tables:
            add_tables_to_pdf(pdf, tables, logos)
    if not content_added:
        print("No content was added to the PDF. The file will not be created.")
