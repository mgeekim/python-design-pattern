from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


class Component(ABC):
    """
    베이스 Component 클래스는 구성의 간단한 객체와 복합 객체 모두에 대한 공통 작업을 선언합니다.
    """

    @property
    def parent(self) -> Component:
        return self._parent

    @parent.setter
    def parent(self, parent: Component):
        """
        선택적으로, 베이스 Component는 구성 요소의 부모를 설정하고 액세스하기 위한 인터페이스를 선언할 수 있습니다.
        이러한 메서드들에 대한 일부 기본 구현을 제공할 수도 있습니다.
        """

        self._parent = parent

    """
    경우에 따라 베이스 Component 클래스에 자식 관리 작업을 직접 정의하는 것이 유용할 수 있습니다.
    이렇게 하면 객체 트리 조립 중에도 구체적인 구성 요소 클래스를 클라이언트 코드에 노출시키지 않아도 됩니다.
    하지만 잎 수준의 구성 요소에 대해 이러한 메서드는 빈 상태가 될 것입니다.
    """

    def add(self, component: Component) -> None:
        pass

    def remove(self, component: Component) -> None:
        pass

    def is_composite(self) -> bool:
        """
        구성 요소가 자식을 가질 수 있는지 여부를 클라이언트 코드에 알려주는 메서드를 제공할 수 있습니다.
        """

        return False

    @abstractmethod
    def operation(self) -> str:
        """
        베이스 Component는 기본 동작을 구현하거나 (해당 동작을 포함하는 메서드를 "추상"으로 선언함으로써)
        구체적인 클래스에게 남겨둘 수 있습니다.
        """

        pass


class Leaf(Component):
    """
    Leaf 클래스는 구성의 끝 객체를 나타냅니다. Leaf는 자식을 가질 수 없습니다.

    일반적으로 Leaf 객체가 실제 작업을 수행하며, Composite 객체는 자식 구성 요소로 위임합니다.
    """

    def operation(self) -> str:
        return "Leaf"


class Composite(Component):
    """
    Composite 클래스는 자식을 가질 수 있는 복합 구성 요소를 나타냅니다.
    일반적으로 Composite 객체는 실제 작업을 자식에게 위임한 후 결과를 "합산"합니다.
    """

    def __init__(self) -> None:
        self._children: List[Component] = []

    """
    복합 객체는 자식을 자신의 자식 목록에 추가하거나 제거할 수 있습니다.
    """

    def add(self, component: Component) -> None:
        self._children.append(component)
        component.parent = self

    def remove(self, component: Component) -> None:
        self._children.remove(component)
        component.parent = None

    def is_composite(self) -> bool:
        return True

    def operation(self) -> str:
        """
        복합 객체는 특정한 방식으로 주요 로직을 실행합니다.
        이는 재귀적으로 모든 자식을 통과하며 그들의 결과를 수집하고 합산합니다.
        복합 객체의 자식들은 이러한 호출을 그들의 자식들에게 전달하고 이와 같이 전체 객체 트리가 횡단됩니다.
        """

        results = []
        for child in self._children:
            results.append(child.operation())
        return f"Branch({'+'.join(results)})"


def client_code(component: Component) -> None:
    """
    클라이언트 코드는 베이스 인터페이스를 통해 모든 구성 요소를 처리합니다.
    """

    print(f"RESULT: {component.operation()}", end="")


def client_code2(component1: Component, component2: Component) -> None:
    """
    자식 관리 작업이 베이스 Component 클래스에 선언되어 있기 때문에
    클라이언트 코드는 구체적인 클래스에 의존하지 않고도 어떤 구성 요소든 간단한 또는 복합인지 작동할 수 있습니다.
    """

    if component1.is_composite():
        component1.add(component2)

    print(f"RESULT: {component1.operation()}", end="")


if __name__ == "__main__":
    # 이렇게 하면 클라이언트 코드가 간단한 잎 구성 요소를 지원할 수 있습니다...
    simple = Leaf()
    print("Client: 간단한 구성 요소가 있습니다:")
    client_code(simple)
    print("\n")

    # ...또한 복합 객체도 지원할 수 있습니다.
    tree = Composite()

    branch1 = Composite()
    branch1.add(Leaf())
    branch1.add(Leaf())

    branch2 = Composite()
    branch2.add(Leaf())

    tree.add(branch1)
    tree.add(branch2)

    print("Client: 이제 복합 트리를 가지고 있습니다:")
    client_code(tree)
    print("\n")

    print("Client: 객체를 관리할 때 구성 요소 클래스를 확인할 필요가 없습니다:")
    client_code2(tree, simple)
