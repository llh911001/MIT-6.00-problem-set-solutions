# 6.00 Problem Set 12
#
# Name:
# Collaborators:
# Time:

import numpy
import random
import pylab
import collections

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

#
# PROBLEM 1
#

class SimpleVirus(object):
    """
    Representation of a simple virus (does not model drug effects/resistance).
    """

    def __init__(self, max_birth_prob, clear_prob):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.

        max_birth_prob: Maximum reproduction probability (a float between 0-1)

        clear_prob: Maximum clearance probability (a float between 0-1).
        """
        self.max_birth_prob = max_birth_prob
        self.clear_prob = clear_prob

    def doesClear(self):
        """
        Stochastically determines whether this virus is cleared from the
        patient's body at a time step.

        returns: Using a random number generator (random.random()), this method
        returns True with probability self.clear_prob and otherwise returns
        False.
        """
        if random.random() < self.clear_prob:
            return True
        return False

    def reproduce(self, pop_density):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.max_birth_prob * (1 - pop_density).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        max_birth_prob and clear_prob values as its parent).

        pop_density: the population density (a float), defined as the current
        virus population divided by the maximum population.

        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        max_birth_prob and clear_prob values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        reproduce_prob = self.max_birth_prob * (1 - pop_density)
        if random.random() < reproduce_prob:
            return SimpleVirus(self.max_birth_prob, self.clear_prob)
        else:
            raise NoChildException

class SimplePatient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """

    def __init__(self, viruses, max_pop):
        """
        Initialization function, saves the viruses and max_pop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        max_pop: the  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.max_pop = max_pop

    def getTotalPop(self):
        """
        Gets the current total virus population.

        returns: The total virus population (an integer)
        """
        return len(self.viruses)

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:

        - Determine whether each virus particle survives and updates the list
          of virus particles accordingly.

        - The current population density is calculated. This population density
          value is used until the next call to update()

        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.

        returns: the total virus population at the end of the update (an
        integer)
        """
        pop_density = self.getTotalPop() / float(self.max_pop)
        res = []
        for virus in self.viruses:
            if not virus.doesClear():
                res.append(virus)
                try:
                    child = virus.reproduce(pop_density)
                    res.append(child)
                except NoChildException:
                    continue
        self.viruses = res
        return self.getTotalPop()

#
# PROBLEM 2
#

def problem2():
    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).

    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.
    """
    viruses = [SimpleVirus(0.1, 0.05) for i in range(100)]
    patient = SimplePatient(viruses, 1000)
    pop_result = []
    for n in range(300):
        num_viruses = patient.update()
        pop_result.append(num_viruses)
    #return pop_result
    pylab.plot(range(1, 301), pop_result)
    pylab.xticks(range(0, 301, 50))
    pylab.xlabel('Timesteps')
    pylab.ylabel('Total population')
    pylab.title('Total virus population in SimplePatient(without drugs treatment) vs time steps')

    pylab.show()

#problem2()

#
# PROBLEM 3
#

class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """

    def __init__(self, max_birth_prob, clear_prob, resistances, mut_prob):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        max_birth_prob: Maximum reproduction probability (a float between 0-1)

        clear_prob: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mut_prob: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        self.max_birth_prob = max_birth_prob
        self.clear_prob = clear_prob
        self.resistances = resistances
        self.mut_prob = mut_prob

    def getResistance(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.

        drug: the drug (a string).

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        return self.resistances.get(drug, False)

    def reproduce(self, pop_density, active_drugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in active_drugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:

        self.max_birth_prob * (1 - pop_density).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        max_birth_prob and clear_prob values as its parent).

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mut_prob of
        inheriting that resistance trait from the parent, and probability
        mut_prob of switching that resistance trait in the offspring.

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mut_prob` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        pop_density: the population density (a float), defined as the current
        virus population divided by the maximum population

        active_drugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        max_birth_prob and clear_prob values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        for drug in active_drugs:
            if not self.getResistance(drug):
                raise NoChildException

        reproduce_prob = self.max_birth_prob * (1 - pop_density)
        if random.random() < reproduce_prob:
            child_resistances = {}
            for prd, tof in self.resistances.items():
                if random.random() < self.mut_prob:
                    child_resistances[prd] = not tof
                else:
                    child_resistances[prd] = tof
            return ResistantVirus(self.max_birth_prob, self.clear_prob, child_resistances, self.mut_prob)
        else:
            raise NoChildException


class Patient(SimplePatient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, max_pop):
        """
        Initialization function, saves the viruses and max_pop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        max_pop: the  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.max_pop = max_pop
        self.active_drugs = set()

    def addPrescription(self, new_drug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        new_drug is already prescribed to this patient, the method has no effect.

        new_drug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        self.active_drugs.add(new_drug)

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return list(self.active_drugs)

    def getResistPop(self, drug_resist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drug_resist.

        drug_resist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drug_resist list.
        """
        count = 0
        for virus in self.viruses:
            resist_to_all = True
            for drug in drug_resist:
                if not virus.getResistance(drug):
                    resist_to_all = False
            if resist_to_all:
                count += 1
        return count


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: the total virus population at the end of the update (an
        integer)
        """
        pop_density = self.getTotalPop() / float(self.max_pop)
        res = []
        for virus in self.viruses:
            if not virus.doesClear():
                res.append(virus)
                try:
                    child = virus.reproduce(pop_density, self.getPrescriptions())
                    res.append(child)
                except NoChildException:
                    continue
        self.viruses = res
        return self.getTotalPop()

#
# PROBLEM 4
#

def problem4():
    """
    Runs simulations and plots graphs for problem 4.

    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.

    total virus population vs. time  and guttagonol-resistant virus population
    vs. time are plotted
    """
    viruses = [ResistantVirus(0.1, 0.05, {'guttagonol': False}, 0.005) for _ in range(100)]
    patient = Patient(viruses, 1000)

    total_pop = []
    resist_pop = []
    for n in range(300):
        total = patient.update()
        resist = patient.getResistPop(['guttagonol'])
        if n == 150:
            patient.addPrescription('guttagonol') # add guttagonol to patient
        total_pop.append(total)
        resist_pop.append(resist)

    pylab.plot(range(1,301), total_pop, color='blue', label='total virus population')
    pylab.plot(range(1, 301), resist_pop, color='green', label='guttagonol-resistent population')
    #pylab.xticks(range(0, 301, 50))
    pylab.xlabel('Timesteps')
    pylab.ylabel('Virus population')
    pylab.title('Total and guttagonol-resistant virus population(at time 150 guttagonol added) vs time steps')
    pylab.legend(loc='upper left')

    F = pylab.gcf()
    default_size = F.get_size_inches()
    F.set_size_inches((default_size[0]*1.5, default_size[1]*1.5))

    pylab.show()

#problem4()

#
# PROBLEM 5
#

def problem5():
    """
    Runs simulations and make histograms for problem 5.

    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).
    """
    viruses = [ResistantVirus(0.1, 0.05, {'guttagonol': False}, 0.005) for _ in range(100)]
    num_trials = 100
    print '\n%d patients -- run the sumulation for 300, 150, 75 and 0 time steps before administering guttagonol, each for %d patients\n' % (num_trials, num_trials)

    delays = collections.defaultdict(list) # a dict of list, which contains the final virus population of each trial(patient)

    for steps, delay in [(450,300), (300,150), (225,75), (150,0)]:
        print '%d patients, %d time steps, treat, 150 more time steps\n' % (num_trials, delay)
        for n in range(num_trials):
            patient = Patient(viruses, 1000)
            for i in range(steps):
                total = patient.update()
                if i == delay:
                    patient.addPrescription('guttagonol')
            delays[delay].append(total)

    cuered_rates = {}
    for k, v in delays.items():
        cuered = [p for p in v if p <= 50]
        cuered_rates[k] = str(100 * len(cuered) / float(len(v))) + '%'

    for delay in [300, 150, 75, 0]:
        pylab.figure()
        pylab.hist(delays[delay])
        pylab.title('Treatment at %d (followed by 150 time steps treatment)' % delay)
        pylab.xlabel('Final total virus population -- %s cuered' % cuered_rates[delay])
        pylab.ylabel('Number of patients')

    pylab.show()

#problem5()

#
# PROBLEM 6
#

def problem6():
    """
    Runs simulations and make histograms for problem 6.

    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """
    viruses = [ResistantVirus(0.1, 0.05, {'guttagonol':False, 'grimpex':False}, 0.005) for _ in range(100)]
    num_trials = 30
    print '\n%d patients -- 150 time steps, add guttagonol, 300, 150, 75 and 0 time steps, add grimpex, 150 more time steps\n' % num_trials

    delays = collections.defaultdict(list) # a dict of list, which contains the final virus population of each trial(patient)

    for steps, delay in [(600,300), (450,150), (375,75), (300,0)]:
        print '%d patients, 150 time steps, add guttagonol, %d time steps, add grimpex, 150 more time steps\n' % (num_trials, delay)
        for n in range(num_trials):
            patient = Patient(viruses, 1000)
            for i in range(steps):
                total = patient.update()
                if i == 150:
                    patient.addPrescription('guttagonol')
                if i  == delay + 150:
                    patient.addPrescription('grimpex')
            delays[delay].append(total)

    cuered_rates = {}
    for k, v in delays.items():
        cuered = [p for p in v if p <= 50]
        cuered_rates[k] = str(100 * len(cuered) / float(len(v))) + '%'

    for delay in [300, 150, 75, 0]:
        pylab.figure()
        pylab.hist(delays[delay])
        pylab.title('%d patients, 150 time steps, add guttagonol, %d time steps, add grimpex, more 150 time steps' % (delay, delay))
        pylab.xlabel('Final total virus population -- %s cuered' % cuered_rates[delay])
        pylab.ylabel('Number of patients')

    pylab.show()

#problem6()

#
# PROBLEM 7
#

def problem7():
    """
    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.

    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.
    """
    viruses = [ResistantVirus(0.1, 0.05, {'guttagonol':False, 'grimpex':False}, 0.005) for _ in range(100)]

    print '150 time steps, add guttagonol, 300 time steps, add grimpex, 150 more time steps\n'
    patient = Patient(viruses, 1000)
    total_pop = []
    resist_guttagonol_pop = []
    resist_grimpex_pop = []
    resist_both_pop = []
    for i in range(600):
        total_pop.append(patient.update())
        resist_guttagonol_pop.append(patient.getResistPop(['guttagonol']))
        resist_grimpex_pop.append(patient.getResistPop(['grimpex']))
        resist_both_pop.append(patient.getResistPop(['guttagonol', 'grimpex']))
        if i == 150:
            patient.addPrescription('guttagonol')
        if i  == 450:
            patient.addPrescription('grimpex')

    pylab.figure()
    pylab.plot(range(1,601), total_pop, color='red', label='total virus population')
    pylab.plot(range(1,601), resist_guttagonol_pop, color='blue', label='guttagonol-resistant')
    pylab.plot(range(1,601), resist_grimpex_pop, color='yellow', label='grimpex-resistant')
    pylab.plot(range(1,601), resist_both_pop, color='green', label='both resistant')
    #pylab.xticks(range(0,601,100))
    pylab.xlabel('Timesteps')
    pylab.ylabel('Virus population')
    pylab.title('150 time steps, add guttagonol, 300 time steps, add grimpex, 150 more time steps')
    pylab.legend(loc='upper left')


    print '150 time steps, add guttagonol and grimpex simultaneoulsy, 150 more time steps'
    patient = Patient(viruses, 1000)
    total_pop = []
    resist_guttagonol_pop = []
    resist_grimpex_pop = []
    resist_both_pop = []
    for i in range(300):
        total_pop.append(patient.update())
        resist_guttagonol_pop.append(patient.getResistPop(['guttagonol']))
        resist_grimpex_pop.append(patient.getResistPop(['grimpex']))
        resist_both_pop.append(patient.getResistPop(['guttagonol', 'grimpex']))
        if i == 150:
            patient.addPrescription('guttagonol')
            patient.addPrescription('grimpex')

    pylab.figure()
    pylab.plot(range(1,301), total_pop, color='red', label='total virus population')
    pylab.plot(range(1,301), resist_guttagonol_pop, color='blue', label='guttagonol-resistant')
    pylab.plot(range(1,301), resist_grimpex_pop, color='yellow', label='grimpex-resistant')
    pylab.plot(range(1,301), resist_both_pop, color='green', label='both resistant')
    #pylab.xticks(range(0,601,100))
    pylab.xlabel('Timesteps')
    pylab.ylabel('Virus population')
    pylab.title('150 time steps, add guttagonol and grimpex simultaneoulsy, 150 more time steps')
    pylab.legend(loc='upper right')

    pylab.show() # show the figure


problem7()
