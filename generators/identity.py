from nio.common.signal.base import Signal


class IdentityGenerator():

    def generate_signals(self, n=1):
        return (Signal() for i in range(n))
