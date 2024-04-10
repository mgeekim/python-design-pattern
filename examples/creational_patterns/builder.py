from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Builder(ABC):
    """
    빌더 인터페이스는 Product 객체의 다른 부분들을 생성하기 위한 메서드를 지정합니다.
    """

    @property
    @abstractmethod
    def product(self) -> None:
        pass

    @abstractmethod
    def produce_part_a(self) -> None:
        pass

    @abstractmethod
    def produce_part_b(self) -> None:
        pass

    @abstractmethod
    def produce_part_c(self) -> None:
        pass


class ConcreteBuilder1(Builder):
    """
    Concrete Builder 클래스들은 Builder 인터페이스를 따르며, 빌딩 단계의 구체적인 구현을 제공합니다.
    프로그램에는 여러 가지 형태의 Builder가 있을 수 있습니다.
    """

    def __init__(self) -> None:
        """
        새로운 빌더 인스턴스는 공백 상태의 product 객체를 포함해야 합니다. 이는 후속 조립에서 사용됩니다.
        """
        self.reset()

    def reset(self) -> None:
        self._product = Product1()

    @property
    def product(self) -> Product1:
        """
        Concrete Builder는 결과를 검색하기 위한 자체 메서드를 제공해야 합니다.
        이는 여러 가지 타입의 빌더가 서로 다른 인터페이스를 따르는 완전히 다른 제품을 생성할 수 있기 때문입니다.
        따라서 이러한 메서드는 기본 Builder 인터페이스에 선언될 수 없습니다.
        일반적으로 클라이언트에 결과를 반환한 후에는 빌더 인스턴스가 새로운 제품을 생산할 준비가 되어야 합니다.
        이것이 getProduct 메서드의 몸체 끝에서 reset 메서드를 호출하는 일반적인 관행입니다.
        그러나 이 동작은 필수가 아니며, 이전 결과를 폐기하기 전에 클라이언트 코드로부터 명시적인 reset 호출을 기다릴 수 있습니다.
        """
        product = self._product
        self.reset()
        return product

    def produce_part_a(self) -> None:
        self._product.add("PartA1")

    def produce_part_b(self) -> None:
        self._product.add("PartB1")

    def produce_part_c(self) -> None:
        self._product.add("PartC1")


class Product1():
    """
    제품이 매우 복잡하고 다양한 구성을 요구할 때에만 빌더 패턴을 사용하는 것이 합리적입니다.
    다른 생성 패턴과 달리, 서로 관련 없는 제품을 생성할 수 있는 경우가 있습니다.
    """

    def __init__(self) -> None:
        self.parts = []

    def add(self, part: Any) -> None:
        self.parts.append(part)

    def list_parts(self) -> None:
        print(f"제품 부품들: {', '.join(self.parts)}", end="")


class Director:
    """
    디렉터는 특정 순서나 구성에 따라 빌딩 단계를 실행하는 것만 책임집니다.
    특정한 주문이나 구성에 따라 제품을 생성할 때 유용합니다.
    엄밀히 말하면 디렉터 클래스는 선택적입니다. 클라이언트는 빌더를 직접 제어할 수 있습니다.
    """

    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        """
        디렉터는 클라이언트 코드가 전달하는 모든 빌더 인스턴스와 함께 작동합니다.
        따라서 클라이언트 코드는 새로 생성되는 제품의 최종 유형을 변경할 수 있습니다.
        """
        self._builder = builder

    """
    디렉터는 동일한 빌딩 단계를 사용하여 여러 가지 제품을 만들 수 있습니다.
    """

    def build_minimal_viable_product(self) -> None:
        self.builder.produce_part_a()

    def build_full_featured_product(self) -> None:
        self.builder.produce_part_a()
        self.builder.produce_part_b()
        self.builder.produce_part_c()


if __name__ == "__main__":
    """
    클라이언트 코드는 빌더 객체를 생성하고, 디렉터에게 전달한 후, 건설 프로세스를 시작합니다.
    최종 결과물은 빌더 객체에서 검색됩니다.
    """

    director = Director()
    builder = ConcreteBuilder1()
    director.builder = builder

    print("기본 표준 제품: ")
    director.build_minimal_viable_product()
    builder.product.list_parts()

    print("\n")

    print("표준 full featured 제품: ")
    director.build_full_featured_product()
    builder.product.list_parts()

    print("\n")

    # 빌더 패턴은 디렉터 클래스 없이도 사용할 수 있습니다.
    print("사용자 정의 제품: ")
    builder.produce_part_a()
    builder.produce_part_b()
    builder.product.list_parts()
