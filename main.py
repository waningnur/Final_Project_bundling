import os
import sys
import streamlit as st
import pandas as pd
from itertools import combinations
from collections import defaultdict
from io import BytesIO,StringIO


st.title('Cari Produk Yang Sering Dibeli Bersamaan')
st.write("Tabel csv berisi ID_TRANSAKSI dan ITEMS")


class FileUpload(object):
    def __init__(self):
        self.FileTypes = ["csv"]

    def run(self):
        st.info(_doc_)
        file = st.file_uploader("upload file", type = self.FileTypes)
        show_file = st.empty()
        if not file:
            show_file.info("Please upload a file of type : "+",".join(["csv"]))
            return
        content = file.getvalue()
        if isinstance(file,BytesIO):
            if olah :
                data = pd.read_csv(file, delimiter=';')
                st.dataframe(data.head(10))

                # Ensure data is properly formatted
                data['ITEMS'] = data['ITEMS'].apply(lambda x: [item.strip() for item in x.split(',')])

                # Prepare transactions list for Apriori
                transactions = data['ITEMS'].tolist()

                # Parameter
                min_support = 0.1  # Minimum support (30%)
                n_transactions = len(transactions)

                # Fungsi untuk menghitung Frequent Itemsets
                def get_frequent_itemsets(transactions, min_support):
                    item_support = defaultdict(int)

                    # Menghitung jumlah kemunculan itemset
                    for transaction in transactions:
                        for size in range(2, len(transaction) + 1):  # Hanya pasangan atau lebih
                            for itemset in combinations(transaction, size):
                                item_support[frozenset(itemset)] += 1

                    # Filter itemset berdasarkan min_support
                    frequent_itemsets = {
                        itemset: count / n_transactions
                        for itemset, count in item_support.items()
                        if count / n_transactions >= min_support
                    }

                    return frequent_itemsets

                # Eksekusi
                frequent_itemsets = get_frequent_itemsets(transactions, min_support)

                # Membuat DataFrame untuk hasil yang lebih rapi
                results_df = pd.DataFrame(list(frequent_itemsets.items()), columns=['Itemset', 'Support'])
                results_df['Itemset'] = results_df['Itemset'].apply(lambda x: set(x)) # Convert frozenset to set

                # Mengurutkan berdasarkan Support secara menurun
                results_df = results_df.sort_values(by='Support', ascending=False)

                # Menampilkan hasil dalam bentuk tabel
                st.write("Frequent Itemsets (Item yang sering dibeli bersama):  ", results_df)
                
                # Tampilkan hasil
                
                    


        file.close()

olah = st.button ("Cari Bundling")


    



if __name__ == "__main__":
    helper = FileUpload()
    helper.run()

