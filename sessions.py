from datetime import datetime
from enum import Enum, auto
from typing import List, Tuple

from sqlalchemy.orm import Session

import backend
from backend import Dataset, ImageSlice
from model import LabelSession, SessionElement


class LabelSessionType(Enum):
    CATEGORICAL_IMAGE = auto()
    CATEGORICAL_SLICE = auto()
    COMPARISON_SLICE = auto()


def create_categorical_image_session(session: Session, name: str, prompt: str,
                                     dataset: Dataset, label_values: List[str]):
    label_session = LabelSession(
        dataset=dataset.name,
        session_name=name,
        session_type=LabelSessionType.CATEGORICAL_IMAGE.name,
        prompt=prompt,
        date_created=datetime.now(),
        label_values_str=','.join(label_values)
    )

    session.add(label_session)

    images = backend.get_images(dataset)
    for i, im in enumerate(images):
        el = SessionElement(
            element_index=i,
            image_1_name=im.name,
            session=label_session
        )
        session.add(el)

    session.commit()


def create_categorical_slice_session(session: Session, name: str, prompt: str,
                                     dataset: Dataset, label_values: List[str], slices: List[ImageSlice]):
    label_session = LabelSession(
        dataset=dataset.name,
        session_name=name,
        session_type=LabelSessionType.CATEGORICAL_SLICE.name,
        prompt=prompt,
        date_created=datetime.now(),
        label_values_str=','.join(label_values)
    )

    session.add(label_session)

    for i, sl in enumerate(slices):
        el = SessionElement(
            element_index=i,
            image_1_name=sl.image_name,
            slice_1_index=sl.slice_index,
            slice_1_type=sl.slice_type.name,
            session=label_session
        )
        session.add(el)

    session.commit()


def create_comparison_slice_session(session: Session, name: str, prompt: str,
                                    dataset: Dataset, label_values: List[str],
                                    comparisons: List[Tuple[ImageSlice, ImageSlice]]):
    label_session = LabelSession(
        dataset=dataset.name,
        session_name=name,
        session_type=LabelSessionType.COMPARISON_SLICE.name,
        prompt=prompt,
        date_created=datetime.now(),
        label_values_str=','.join(label_values)
    )

    session.add(label_session)

    for i, (sl1, sl2) in enumerate(comparisons):
        el = SessionElement(
            element_index=i,
            image_1_name=sl1.image_name,
            slice_1_index=sl1.slice_index,
            slice_1_type=sl1.slice_type.name,
            image_2_name=sl2.image_name,
            slice_2_index=sl2.slice_index,
            slice_2_type=sl2.slice_type.name,
            session=label_session
        )
        session.add(el)

    session.commit()