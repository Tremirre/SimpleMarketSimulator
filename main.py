from sim.simulation import Simulation


def main():
    simulation = Simulation(20, 10)
    simulation.run(365)


if __name__ == "__main__":
    main()
