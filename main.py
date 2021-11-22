from sim.simulation import Simulation


def main():
    super_folder = "DS4\\"
    folders = ["10_investors\\", "50_investors\\", "100_investors\\"]
    investor_sizes = [10, 50, 100]
    tries = 4
    for folder, size in zip(folders, investor_sizes):
        for i in range(tries):
            simulation = Simulation(size, 20, super_folder + folder + f"prices{i+1}.txt")
            simulation.run(720)
            simulation.export()
    #simulation = Simulation(10, 10)
    #simulation.run(365)


if __name__ == "__main__":
    main()
