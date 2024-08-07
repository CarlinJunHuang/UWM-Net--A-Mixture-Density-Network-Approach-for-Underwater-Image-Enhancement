from pathlib import Path
from typing import Callable, Optional

import pytorch_lightning as pl
from torch.utils.data import DataLoader, Dataset

from src.datasets.meta import ExtendedPairedImageWithLightnessInput  # noqa: I900
from src.transforms import load_transforms  # noqa: I900
from src.utils.image import read_image_cv2  # noqa: I900


class UIEB(Dataset):
    MAPPING = {
        'train': 'train',
        'val': 'val',
        'test': 'test',
    }

    def __init__(
        self,
        root: Path,
        pair_transform: Callable,
        split: str = "train",
        preload: bool = False,
        start_idx: int = 0,
        limit: Optional[int] = None,
    ):
        path = root / UIEB.MAPPING[split]

        self.pair_transform = pair_transform

        self.image_names = sorted(
            (path / "low/").glob("*.png"), key=lambda x: int(x.stem)
        )
        self.target_names = sorted(
            (path / "high/").glob("*.png"), key=lambda x: int(x.stem)
        )

        if limit is not None:
            self.image_names = self.image_names[start_idx:start_idx+limit]
            self.target_names = self.target_names[start_idx:start_idx+limit]

        self.loaded = preload
        if self.loaded:
            self.load_all_images()

    def load_all_images(self) -> None:
        self.loaded_images_ = []
        self.loaded_targets_ = []

        for index in range(len(self)):
            self.loaded_images_.append(read_image_cv2(self.image_names[index]))
            self.loaded_targets_.append(read_image_cv2(self.target_names[index]))

    def __len__(self) -> int:
        return len(self.image_names)

    def __getitem__(self, index: int) -> ExtendedPairedImageWithLightnessInput:

        image = (
            self.loaded_images_[index]
            if self.loaded
            else read_image_cv2(self.image_names[index])
        )
        target = (
            self.loaded_targets_[index]
            if self.loaded
            else read_image_cv2(self.target_names[index])
        )

        transformed = self.pair_transform(image=image, target=target)
        image, target = transformed["image"], transformed["target"]

        source_lightness = transformed["source_lightness"]
        target_lightness = transformed["target_lightness"]

        return {
            "image": image,
            "target": target,
            "source_lightness": source_lightness,
            "target_lightness": target_lightness,
            "image_name": self.image_names[index].name,
            "target_name": self.target_names[index].name,
        }


class UIEBDataModule(pl.LightningDataModule):
    def __init__(self, config):
        super().__init__()
        self.root = Path(config.path)
        self.config = config

        self.train_transform, self.test_transform = load_transforms(config.transform)

    def setup(self, stage: Optional[str] = None):
        self.train_ds = UIEB(
            self.root,
            split='train',
            pair_transform=self.train_transform,
            preload=self.config.preload,
            start_idx=self.config.start_idx,
            limit=self.config.limit,
        )

        self.val_ds = UIEB(
            self.root,
            split='val',
            pair_transform=self.test_transform,
            preload=self.config.preload,
        )

        self.test_ds = UIEB(
            self.root,
            split='test',
            pair_transform=self.test_transform,
            preload=self.config.preload,
        )

    def train_dataloader(self):
        return DataLoader(
            self.train_ds,
            batch_size=self.config.batch_size,
            pin_memory=self.config.pin_memory,
            num_workers=self.config.num_workers,
            shuffle=True,
        )

    def val_dataloader(self):
        return DataLoader(
            self.val_ds,
            batch_size=self.config.batch_size,
            pin_memory=self.config.pin_memory,
            num_workers=self.config.num_workers,
        )

    def test_dataloader(self):
        return DataLoader(
            self.test_ds,
            batch_size=self.config.batch_size,
            pin_memory=self.config.pin_memory,
            num_workers=self.config.num_workers,
        )


    def predict_dataloader(self):
        return self.test_dataloader()
