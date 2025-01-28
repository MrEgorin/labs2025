import re

"""Важливо: не працює для CRISPR/Cas12a нуклеазою!"""
def find_gRNA(dna_sequence, pam="NGG", gRNA_length=20, gc_content_range=(40, 60)):
    """
    Знаходить можливі gRNA у послідовності ДНК.
    
    :param dna_sequence: ДНК-послідовність (5' -> 3')
    :param pam: PAM-послідовність (використовує регулярні вирази, N означає будь-який нуклеотид)
    :param gRNA_length: Довжина gRNA (без урахування PAM)
    :param gc_content_range: Діапазон GC-вмісту (%), наприклад, (40, 60)
    :return: Список можливих gRNA із їх характеристиками
    """
    # Переведення послідовності ДНК у верхній регістр
    dna_sequence = dna_sequence.upper()
    # Підготовка регулярного виразу для PAM
    pam_regex = pam.replace("N", "[ACGT]")
    # Зберігати можливі gRNA
    potential_gRNAs = []

    # Пошук PAM у послідовності
    for match in re.finditer(pam_regex, dna_sequence):
        pam_start = match.start()
        pam_end = match.end()

        # Витяг послідовності gRNA
        if pam_start >= gRNA_length:
            gRNA_start = pam_start - gRNA_length
            gRNA = dna_sequence[gRNA_start:pam_start]
            pam_seq = dna_sequence[pam_start:pam_end]

            # Обчислення GC-вмісту
            gc_count = gRNA.count("G") + gRNA.count("C")
            gc_content = (gc_count / gRNA_length) * 100

            # Перевірка GC-вмісту на відповідність діапазону
            if gc_content_range[0] <= gc_content <= gc_content_range[1]:
                potential_gRNAs.append({
                    "gRNA": gRNA,
                    "PAM": pam_seq,
                    "Position": (gRNA_start + 1, pam_end),  # Вказати позиції у форматі 1-based
                    "GC_Content": round(gc_content, 2)
                })

    return potential_gRNAs


if __name__ == "__main__":
    # Введення послідовності ДНК через термінал
    dna_sequence = input("Введіть послідовність ДНК (5' -> 3'): ").strip()
    
    # Виклик функції
    results = find_gRNA(dna_sequence)
    
    # Виведення результатів
    if results:
        print("\nЗнайдено можливі gRNA:")
        for idx, gRNA_info in enumerate(results, 1):
            print(f"{idx}. gRNA: {gRNA_info['gRNA']}, PAM: {gRNA_info['PAM']}, "
                  f"Позиція: {gRNA_info['Position']}, GC-вміст: {gRNA_info['GC_Content']}%")
    else:
        print("Можливих gRNA не знайдено.")
