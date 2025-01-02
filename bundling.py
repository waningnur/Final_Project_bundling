import os
import sys
import streamlit as st
import pandas as pd
from itertools import combinations
from collections import defaultdict


st.title('Cari Produk Yang Sering Dibeli Bersamaan dengan Apriori')
st.write("Tabel CSV berisi kolom ID_TRANSAKSI dan ITEMS (dengan ITEMS dipisahkan oleh koma).")

class AprioriApp(object):
    def __init__(self):
        self.file_types = ["csv"]

    def run(self):
        st.info("Upload file CSV untuk mencari item yang sering dibeli bersama.")
        file = st.file_uploader("Upload file", type = self.file_types)
        if not file:
            st.warning("Silakan unggah file dengan format CSV.")
            return

        data = pd.read_csv(file, delimiter=';')
        st.dataframe(data.head(10))

        # Pastikan data diformat dengan benar
        data['ITEMS'] = data['ITEMS'].apply(lambda x: [item.strip() for item in x.split(',')])

        # Ambil transaksi
        transactions = data['ITEMS'].tolist()

        # Parameter
        min_support = st.slider("Minimum Support (%)", 1, 100, 5) / 100  # Slider untuk memilih minimum support
        st.write(f"Minimum Support: {min_support * 100}%")
        n_transactions = len(transactions)

        # Fungsi untuk menghitung frequent itemsets
        def apriori(transactions, min_support):
            def get_frequent_itemsets(candidates, transactions, min_support):
                counts = defaultdict(int)

                # Hitung support kandidat itemsets
                for transaction in transactions:
                    for candidate in candidates:
                        if candidate.issubset(transaction):
                            counts[candidate] += 1

                # Filter itemsets berdasarkan minimum support
                frequent_itemsets = {
                    itemset: count / n_transactions
                    for itemset, count in counts.items()
                    if count / n_transactions >= min_support
                }
                return frequent_itemsets

            # Tahap 1: Frequent 1-Itemset
            single_items = {frozenset([item]) for transaction in transactions for item in transaction}
            frequent_itemsets = get_frequent_itemsets(single_items, transactions, min_support)

            # Iterasi untuk mendapatkan k-Itemset
            all_frequent_itemsets = dict(frequent_itemsets)
            k = 2
            while frequent_itemsets:
                # Buat kandidat k-Itemset dari frequent (k-1)-Itemset
                candidates = {
                    itemset1.union(itemset2)
                    for itemset1 in frequent_itemsets
                    for itemset2 in frequent_itemsets
                    if len(itemset1.union(itemset2)) == k
                }

                # Hitung frequent k-Itemset
                frequent_itemsets = get_frequent_itemsets(candidates, transactions, min_support)

                # Tambahkan ke hasil akhir
                all_frequent_itemsets.update(frequent_itemsets)
                k += 1

            return all_frequent_itemsets

        # Eksekusi Apriori
        frequent_itemsets = apriori(transactions, min_support)

        # Membuat DataFrame untuk hasil yang lebih rapi
        results_df = pd.DataFrame(list(frequent_itemsets.items()), columns=['Itemset', 'Support'])
        results_df['Itemset'] = results_df['Itemset'].apply(lambda x: set(x))  # Konversi frozenset ke set

        # Urutkan berdasarkan Support secara menurun
        results_df = results_df.sort_values(by='Support', ascending=False)

        # Tampilkan hasil
        st.write("Frequent Itemsets (Item yang sering dibeli bersama):", results_df)

        # Unduh hasil
        csv = results_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Hasil CSV", data=csv, file_name="frequent_itemsets.csv", mime="text/csv")


if __name__ == "__main__":
    app = AprioriApp()
    app.run()
