class Target:
    """
    Target은 클라이언트 코드에서 사용하는 도메인별 인터페이스를 정의합니다.
    """

    def request(self) -> str:
        return "Target: 기본 타겟 동작."


class Adaptee:
    """
    Adaptee에는 유용한 동작이 포함되어 있지만, 그 인터페이스는 기존 클라이언트 코드와 호환되지 않습니다.
    Adaptee는 클라이언트 코드가 사용할 수 있도록 어댑션되어야 합니다.
    """

    def specific_request(self) -> str:
        return ".eetpadA eht fo roivaheb laicepS"


class Adapter(Target, Adaptee):
    """
    Adapter는 다중 상속을 통해 Adaptee의 인터페이스를 Target의 인터페이스와 호환되도록 만듭니다.
    """

    def request(self) -> str:
        return f"Adapter: (번역됨) {self.specific_request()[::-1]}"


def client_code(target: "Target") -> None:
    """
    클라이언트 코드는 Target 인터페이스를 따르는 모든 클래스를 지원합니다.
    """

    print(target.request(), end="")


if __name__ == "__main__":
    print("클라이언트: Target 객체와 잘 작동합니다:")
    target = Target()
    client_code(target)
    print("\n")

    adaptee = Adaptee()
    print("클라이언트: Adaptee 클래스의 인터페이스가 이상합니다. "
          "내가 이해하지 못해요:")
    print(f"Adaptee: {adaptee.specific_request()}", end="\n\n")

    print("클라이언트: 하지만 Adapter를 통해 작업할 수 있어요:")
    adapter = Adapter()
    client_code(adapter)
