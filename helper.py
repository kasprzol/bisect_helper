import collections.abc
import typing
from abc import abstractmethod
from typing import overload, Sequence  # _T_co


_T_co = typing.TypeVar("_T_co", covariant=True)  # Any type covariant containers.


class BisectHelper(collections.abc.Sequence):
    @overload
    @abstractmethod
    def __getitem__(self, i: int) -> _T_co:
        ...

    @overload
    @abstractmethod
    def __getitem__(self, s: slice) -> Sequence[_T_co]:
        ...

    def __getitem__(self, i: int) -> _T_co:
        value = self.wrapped_sequence[i]
        for path_component in self.access_path:
            try:
                value = getattr(value, path_component)
                if callable(value):
                    value = value()
            except AttributeError:
                try:
                    try:
                        value = value[path_component]
                    except TypeError:
                        # can't index list with "1", have to use inr("1")
                        # TODO: maybe add a format specifier to access path?
                        value = value[int(path_component)]
                except KeyError:
                    raise LookupError(f"Could not access component {path_component} of {value}")
        return value

    # class BisectHelperIterator(collections.abc.Iterator):
    #
    #     def __init__(self, wrapped_iter: Iterator, access_path: Collection[str]):
    #         self.wrapped_iter = wrapped_iter
    #         self.access_path = access_path
    #
    #     def __next__(self) -> _T_co:
    #         value = next(self.wrapped_iter)
    #         for path_component in self.access_path:
    #             try:
    #                 value = getattr(value, path_component)
    #             except AttributeError:
    #                 value = value[path_component]
    #         return value
    #
    def __init__(self, wrapped_sequence: Sequence, access_path: str):
        self.wrapped_sequence = wrapped_sequence
        self.access_path = access_path.split(".")

    #
    def __len__(self) -> int:
        return len(self.wrapped_sequence)

    # def __iter__(self) -> Iterator[_T_co]:
    #     return BisectHelperIterator(iter(self.wrapped_sequence), self.access_path)
    #
    # def __contains__(self, requested_element: object) -> bool:
    #     for element in self:
    #         if requested_element == element:
    #             return True
    #     return False
