# imdb-analysis# IMDb Analizi (IMDb Analysis)

Bu proje, IMDb film veri seti üzerinde temel veri temizleme, analiz ve görselleştirme işlemleri yaparak film derecelendirmeleri (rating), türler (genre) ve dağılımlar hakkında içgörüler edinmeyi amaçlar.

## 📊 Proje Hedefleri

- IMDb üzerindeki film derecelendirmelerinin dağılımını analiz etmek.  
- Farklı türlerdeki filmlerin IMDb puanlarının nasıl değiştiğini görmek.  
- Veri temizleme adımlarını gerçekleştirmek ve analize hazır bir yapı oluşturmak.  
- Sonuçları görselleştirerek yorumlanabilir grafikler üretmek.

## 📂 Veri

- `movies_initial.csv` adında ham veri dosyası kullanıldı.  
- Veride eksik, tutarsız veya gereksiz kayıtlar temizlendi.  
- Temizlenmiş ve analiz için uygun hale getirilmiş örnek veri dosyası: `Cleaned sample.csv`.

## 🔍 Analiz ve Görselleştirme

Proje kapsamında aşağıdaki analizler ve grafikleri oluşturdum:

1. **Rating Dağılımı**  
   - IMDb puanlarının frekans dağılımını histogram ile gösteriyor.  
   ![Rating Distribution](https://raw.githubusercontent.com/ferhatcelk/imdb-analysis/32907a5dfe2f5c70e962be9ba9116eedf475e201/rating_distribution.png)

2. **Tür Bazlı Rating (Boxplot)**  
   - En popüler türlere göre IMDb puanlarının dağılımını gösteren boxplot.  
   ![Boxplot Ratings by Genre](https://github.com/ferhatcelk/imdb-analysis/raw/32907a5dfe2f5c70e962be9ba9116eedf475e201/boxplot_ratings_by_genre.png)

## 🛠️ Kullanım

1. Depoyu klonlayın:

    ```bash
    git clone https://github.com/ferhatcelk/imdb-analysis.git
    cd imdb-analysis
    ```

2. Gerekli Python bağımlılıklarını yükleyin:

    ```bash
    pip install -r requirements.txt
    ```

3. Analiz betiklerini çalıştırarak veriyi temizleyin ve grafikleri oluşturun.

## ✅ Sonuçlar ve İçgörüler

- Bazı türler (örneğin drama) puan açısından daha yüksek medyan değerine sahip olabilir.  
- Derecelendirme dağılımı grafiği, çoğu filmin orta seviyelerde yoğunlaştığını gösterebilir veya beklenmedik uç değer trendleri ortaya çıkarabilir.  
- Bu analiz, film türü ile izleyici puanı arasında potansiyel korelasyonlar için temel bir başlangıçtır.

## ⚠️ Sınırlamalar ve Gelecek Adımlar

- Veri seti IMDb’nin tam veri tabanı olmayabilir; örnekleme veya filtreleme yapılmış olabilir.  
- Sadece rating analizi yapılmıştır; diğer değişkenler (bütçe, yayın yılı, yönetmen vs.) analiz edilmeyebilir.  
- Gelecekte eklemek için: zaman içinde rating değişimi, tür + yıl ikili analizi, regresyon analizi veya makine öğrenmesi ile puan tahmini.

## 👤 Katkıda Bulunma

- Katkılar, pull request yoluyla memnuniyetle kabul edilir.  
- Lütfen yeni analizler, grafik türleri veya veri işleme geliştirmeleri için issue açın.

## 📄 Lisans

Bu proje MIT Lisansı altındadır. Detaylar için `LICENSE` dosyasına bakabilirsiniz.
