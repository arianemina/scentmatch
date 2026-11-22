# Week 3 - Qualitative recommendation examples

Model: final_nlgcl_notes_rescued_s3.pt

Three real users selected from the training histories.
These examples illustrate recommendation coherence,
not held-out accuracy or a true zero-history cold-start.

## Woody preferences

User index: 22108
Known perfumes: 8

### History

- L'eau Bleue d’Issey Pour Homme by Issey Miyake (ginger, mandarin orange, musk, orange, patchouli, rose)
- Armaf Shades Blue (ambergris, bergamot, cardamom, cedar, citrus accord, geranium)
- RASASI Al Wisam Day (amber, bergamot, cedar, clary sage, geranium, lavender)
- ARMAF The Pride (bergamot, cinnamon, lemon, nutmeg, oakmoss, oriental accord)
- Swiss Arabian Shaghaf (amber, aquatic notes, chypre, fresh notes, lavender, lemon)
- F Armaf Ventana Pour Homme (amber, bergamot, cedar, citrus accord, floral accord, floral notes)
- Versace Pour Homme for Men (bergamot, bitter orange, cedar, citrus accord, clary sage, fruity accord)
- RASASI Hawas (amber, apple, bergamot, cedar, cinnamon, citrus accord)

### Top 3 recommendations

| Perfume | Score | Model explanation |
|---|---:|---|
| Armaf Club de Nuit Man | 0.6284 | Close to RASASI Hawas, which you loved · Shares spicy accord, patchouli and amber with what you love |
| ARMAF TRES NUIT 3.4 | 0.5431 | Shares lemon, spicy accord and sandalwood with what you love · Close to RASASI Hawas, which you loved |
| Bentley Intense B140408 | 0.5225 | Close to RASASI Hawas, which you loved · Shares spicy accord and oriental accord with what you love |

## Sweet preferences

User index: 6903
Known perfumes: 9

### History

- Armaf Club De Nuit Intense (ambergris, apple, bergamot, birch, blackcurrant, fruity accord)
- Sofia Vergara (earthy accord, sandalwood, vanilla)
- Swiss Arabian Shaghaf Oud (oriental accord, oud, rose, saffron, vanilla)
- Lattafa Fakhar for Women (aldehydes, ambroxan, bergamot, floral accord, fruity accord, gardenia)
- OUD VANILLE BY FRANCK OLIVIER (caramel, frankincense, jasmine, musk, orange, oud)
- Lattafa Musk Al Aroos For Women (amber, ambroxan, cedar, floral accord, floral notes, fruity accord)
- Lattafa Ajwad (amber, bergamot, cedar, cinnamon, floral accord, floral notes)
- Lattafa Perfumes Nebras for Unisex (amber, cocoa, mandarin orange, musk, red berries, rose)
- Lattafa Perfumes Khamrah for Unisex (amberwood, benzoin, bergamot, cinnamon, date, myrrh)

### Top 3 recommendations

| Perfume | Score | Model explanation |
|---|---:|---|
| Yara by Lattafa Perfumes | 0.5314 | Shares vanilla, rose and musk with what you love · Close to Lattafa Ajwad, which you loved |
| Lattafa Musk Mood for Unisex | 0.5255 | Shares vanilla, fruity accord and musk with what you love · Close to Lattafa Perfumes Khamrah for Unisex, which you loved |
| Armaf Club De Nuit | 0.5106 | Shares rose and jasmine with what you love · Close to Armaf Club De Nuit Intense, which you loved |

## Limited history (one known perfume)

User index: 0
Known perfumes: 1

### History

- Lattafa Ajwad (amber, bergamot, cedar, cinnamon, floral accord, floral notes)

### Top 3 recommendations

| Perfume | Score | Model explanation |
|---|---:|---|
| Lattafa Fakhar for Women | 0.5605 | Close to Lattafa Ajwad, which you loved · Shares fruity accord, rose and bergamot with what you love |
| Swiss Arabian Shaghaf Oud | 0.5471 | Close to Lattafa Ajwad, which you loved · Shares oriental accord, rose and vanilla with what you love |
| Yara by Lattafa Perfumes | 0.5434 | Close to Lattafa Ajwad, which you loved · Shares pineapple, rose and sandalwood with what you love |
