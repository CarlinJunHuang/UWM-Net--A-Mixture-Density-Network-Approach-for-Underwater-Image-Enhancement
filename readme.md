# UWM-Net: A Mixture Density Network Approach with Minimal Dataset Requirements for Underwater Image Enhancement
### [IEEE CAI 2024](https://ieeecai.org/2024/wp-content/pdfs/540900b498/540900b498.pdf)

Abstract—The learning-based underwater image enhancement,
which is suitable for batch processing, is a pivotal research
direction in underwater image processing. Extensive paired image
data are required in existing learning-based methods, which
necessitate considerable preprocessing and hinder the application
of these methods. To address these limitations, we propose a
semi-supervised approach called UWM-Net: firstly, we use a
compact dataset of underwater image pairs to train the Mixture
Density Network (MDN) with an underwater scene setting;
subsequently, U-Net can learn underwater image enhancement
more efficiently. The MDN can transform standard images into
underwater scenes, reducing the reliance on paired data and
making much smaller training datasets. In experimental studies,
UWM-Net using only 18 pairs of underwater image data achieves
highly competitive results in terms of 3 metrics compared with
advanced models.

![alt text](/images/CAI2024_Poster.png)

## Run the code
To run this code install requirements 
```bash
pip install -r requirements.txt
```
and run the following commands:

```bash
python train_unsupervised.py --config="configs/8shot-lol.yaml"
python finetune.py --config="configs/8shot-lol-ft.yaml"
```
For different config file use --config flag. There are many configs in config folder.


## Acknowledge
Our work are based on the Research of Dimma:
```
@article{kozlowski2023dimma,
  title={Dimma: Semi-supervised Low Light Image Enhancement with Adaptive Dimming},
  author={Koz{\l}owski, Wojciech and Szachniewicz, Micha{\l} and Stypu{\l}kowski, Micha{\l} and Zi{\k{e}}ba, Maciej},
  journal={arXiv preprint arXiv:2310.09633},
  year={2023}
}
```

