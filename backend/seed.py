"""
Seed script — Class 12 NCERT subjects, chapters, quizzes, questions,
placeholder students, and randomised quiz attempts.

Run from the backend folder:
    source venv/bin/activate
    python seed.py
"""

import sys, os, random
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(__file__))
from app import create_app
from app.models import db, User, Subject, Chapter, Quiz, Question, Score

app = create_app()

# ─────────────────────────────────────────────────────────────
# Seed data
# ─────────────────────────────────────────────────────────────

SUBJECTS = [
    {
        "name": "Physics",
        "description": "Electrostatics, current electricity, optics, modern physics & more",
        "chapters": [
            {
                "name": "Electric Charges and Fields",
                "description": "Coulomb's law, electric field lines, Gauss's law",
                "quizzes": [
                    {
                        "title": "Electric Charges — Basics",
                        "description": "Fundamental concepts of charge, Coulomb's law and superposition principle",
                        "time_duration": 15,
                        "questions": [
                            ("The SI unit of electric charge is", "Ampere", "Coulomb", "Farad", "Volt", 2, 1),
                            ("Two equal and opposite charges separated by a distance form a", "Monopole", "Quadrupole", "Dipole", "Tripole", 3, 1),
                            ("Coulomb's law is analogous to", "Ohm's law", "Newton's law of gravitation", "Faraday's law", "Ampere's law", 2, 1),
                            ("The force between two charges is independent of the", "Medium between them", "Magnitude of charges", "Distance between them", "Presence of other charges", 4, 1),
                            ("Quantisation of charge means charge is always a multiple of", "1 C", "1.6×10⁻¹⁹ C", "9×10⁹ C", "6.67×10⁻¹¹ C", 2, 1),
                        ],
                    },
                    {
                        "title": "Electric Field and Gauss's Law",
                        "description": "Electric flux, field due to various charge distributions",
                        "time_duration": 20,
                        "questions": [
                            ("Electric field lines originate from", "Negative charges", "Positive charges", "Neutral bodies", "Conductors only", 2, 1),
                            ("Gauss's law relates electric flux to", "Total charge inside", "Surface area", "Electric potential", "Permittivity only", 1, 1),
                            ("Electric field inside a hollow conductor is", "Maximum", "Zero", "Uniform", "Infinite", 2, 1),
                            ("The number of field lines through a surface represents", "Force", "Flux", "Potential", "Energy", 2, 1),
                            ("SI unit of electric flux is", "N·m²/C", "N/C", "V/m", "C/m²", 1, 1),
                        ],
                    },
                ],
            },
            {
                "name": "Current Electricity",
                "description": "Ohm's law, Kirchhoff's laws, circuits and meters",
                "quizzes": [
                    {
                        "title": "Ohm's Law and Resistance",
                        "description": "V-I characteristics, resistivity, temperature dependence",
                        "time_duration": 15,
                        "questions": [
                            ("Ohm's law states that current is proportional to", "Resistance", "Voltage", "Power", "Charge", 2, 1),
                            ("The SI unit of resistivity is", "Ω", "Ω·m", "S/m", "A/m", 2, 1),
                            ("Resistivity of a conductor increases with temperature because", "More collisions occur", "Fewer electrons present", "Voltage drops", "Mass increases", 1, 1),
                            ("Kirchhoff's current law is based on conservation of", "Energy", "Charge", "Momentum", "Power", 2, 1),
                            ("A Wheatstone bridge is used to measure", "Current", "Voltage", "Resistance", "Capacitance", 3, 1),
                        ],
                    },
                    {
                        "title": "EMF and Internal Resistance",
                        "description": "Cells in series/parallel, terminal voltage, potentiometer",
                        "time_duration": 20,
                        "questions": [
                            ("EMF of a cell is the work done per unit charge in moving charge through", "External circuit", "Internal circuit", "Complete circuit", "Resistor only", 3, 1),
                            ("Terminal voltage is always less than EMF due to", "External resistance", "Internal resistance", "Temperature", "Polarity", 2, 1),
                            ("In a potentiometer the wire should have", "High resistance", "Low resistance per unit length", "High resistivity and uniform cross-section", "Low temperature coefficient", 3, 1),
                            ("Two cells of EMFs E₁ and E₂ in series give a combined EMF of", "E₁ × E₂", "E₁ - E₂", "E₁ + E₂", "E₁ / E₂", 3, 1),
                            ("The internal resistance of an ideal cell is", "Infinite", "Zero", "1 Ω", "Depends on EMF", 2, 1),
                        ],
                    },
                ],
            },
            {
                "name": "Ray Optics and Optical Instruments",
                "description": "Reflection, refraction, lenses, mirrors and optical devices",
                "quizzes": [
                    {
                        "title": "Mirrors and Lenses",
                        "description": "Mirror formula, lens formula, magnification",
                        "time_duration": 20,
                        "questions": [
                            ("The mirror formula is 1/f = 1/v +", "1/u", "1/r", "1/m", "u/v", 1, 1),
                            ("A convex mirror always forms a", "Real, inverted image", "Virtual, erect image", "Real, erect image", "Virtual, inverted image", 2, 1),
                            ("The power of a lens of focal length 50 cm is", "2 D", "5 D", "0.5 D", "50 D", 1, 1),
                            ("Total internal reflection occurs when light travels from", "Rarer to denser medium", "Denser to rarer medium", "Air to water", "Glass to water", 2, 1),
                            ("A compound microscope uses", "One convex lens", "Two concave lenses", "One concave and one convex", "Two convex lenses", 4, 1),
                        ],
                    },
                    {
                        "title": "Wave Optics",
                        "description": "Interference, diffraction and polarisation",
                        "time_duration": 20,
                        "questions": [
                            ("In Young's double slit experiment, fringe width is proportional to", "D/d", "d/D", "λd/D", "D/(λd)", 1, 1),
                            ("Diffraction is most prominent when slit width is", "Much larger than λ", "Comparable to λ", "Much smaller than λ", "Equal to 2λ", 2, 1),
                            ("Polarisation proves light is a", "Longitudinal wave", "Transverse wave", "Sound wave", "Standing wave", 2, 1),
                            ("In constructive interference path difference is", "nλ", "(2n+1)λ/2", "nλ/2", "2nλ", 1, 1),
                            ("Resolving power of a telescope depends on", "Focal length", "Diameter of objective", "Eyepiece power", "Length of tube", 2, 1),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "name": "Chemistry",
        "description": "Solid state, solutions, electrochemistry, organic chemistry & more",
        "chapters": [
            {
                "name": "The Solid State",
                "description": "Crystal structures, unit cells, defects in solids",
                "quizzes": [
                    {
                        "title": "Unit Cells and Crystal Systems",
                        "description": "Bravais lattices, packing efficiency, coordination number",
                        "time_duration": 15,
                        "questions": [
                            ("The number of atoms in a face-centred cubic (FCC) unit cell is", "1", "2", "4", "8", 3, 1),
                            ("Coordination number in a body-centred cubic structure is", "6", "8", "12", "4", 2, 1),
                            ("Schottky defect leads to", "Increase in density", "Decrease in density", "No change in density", "Change in colour", 2, 1),
                            ("NaCl has which type of crystal structure?", "Simple cubic", "BCC", "FCC (rock salt)", "HCP", 3, 1),
                            ("The most efficient packing arrangement is", "Simple cubic", "BCC", "FCC / HCP", "Tetrahedral", 3, 1),
                        ],
                    },
                    {
                        "title": "Defects and Properties of Solids",
                        "description": "Electrical, magnetic, and optical properties",
                        "time_duration": 15,
                        "questions": [
                            ("An n-type semiconductor has excess of", "Holes", "Electrons", "Protons", "Neutrons", 2, 1),
                            ("Ferromagnetic materials when heated above Curie temperature become", "Paramagnetic", "Diamagnetic", "Ferrimagnetic", "Antiferromagnetic", 1, 1),
                            ("Frenkel defect is found in", "NaCl", "AgCl", "KCl", "MgO", 2, 1),
                            ("A piezoelectric crystal produces electric field when", "Heated", "Cooled", "Mechanically stressed", "Dissolved", 3, 1),
                            ("Conductivity of semiconductors increases with temperature because", "Lattice vibrations decrease", "More electron-hole pairs are generated", "Resistance increases", "Band gap widens", 2, 1),
                        ],
                    },
                ],
            },
            {
                "name": "Electrochemistry",
                "description": "Electrochemical cells, Nernst equation, electrolysis",
                "quizzes": [
                    {
                        "title": "Galvanic and Electrolytic Cells",
                        "description": "Cell potential, electrode reactions, Faraday's laws",
                        "time_duration": 20,
                        "questions": [
                            ("In a galvanic cell the anode is", "Positive electrode", "Negative electrode", "Neutral electrode", "Reference electrode", 2, 1),
                            ("The standard hydrogen electrode has a potential of", "1 V", "-1 V", "0 V", "0.5 V", 3, 1),
                            ("Faraday's first law states that mass deposited is proportional to", "Current only", "Time only", "Charge passed", "Voltage applied", 3, 1),
                            ("The Nernst equation gives cell potential at", "Standard conditions", "Non-standard conditions", "Equilibrium only", "High temperature only", 2, 1),
                            ("Rusting of iron is an example of", "Dry corrosion", "Electrochemical corrosion", "Chemical corrosion", "Physical corrosion", 2, 1),
                        ],
                    },
                    {
                        "title": "Conductance and Kohlrausch's Law",
                        "description": "Molar conductance, electrolytes, Debye-Hückel-Onsager",
                        "time_duration": 15,
                        "questions": [
                            ("Specific conductance of a solution", "Increases with dilution", "Decreases with dilution", "Remains constant", "First increases then decreases", 2, 1),
                            ("Molar conductance at infinite dilution for weak electrolytes is determined by", "Direct measurement", "Kohlrausch's law", "Ohm's law", "Faraday's law", 2, 1),
                            ("Strong electrolytes are fully", "Dissociated in solution", "Undissociated", "Partially dissociated", "Ionised only when heated", 1, 1),
                            ("The unit of molar conductance is", "S·cm²/mol", "S/cm", "Ω·cm", "S·cm", 1, 1),
                            ("At infinite dilution, equivalent conductance of NaCl equals", "λ(Na⁺) + λ(Cl⁻)", "λ(Na⁺) × λ(Cl⁻)", "λ(Na⁺) - λ(Cl⁻)", "λ(Na⁺) / λ(Cl⁻)", 1, 1),
                        ],
                    },
                ],
            },
            {
                "name": "Chemical Kinetics",
                "description": "Rate laws, order, activation energy, Arrhenius equation",
                "quizzes": [
                    {
                        "title": "Rate of Reaction and Order",
                        "description": "Rate law, integrated rate equations, half-life",
                        "time_duration": 20,
                        "questions": [
                            ("The order of a reaction is determined by", "Stoichiometry", "Experiment", "Temperature", "Pressure", 2, 1),
                            ("Half-life of a first-order reaction is", "Directly proportional to concentration", "Independent of concentration", "Inversely proportional to concentration", "Dependent on temperature only", 2, 1),
                            ("The unit of rate constant for a first-order reaction is", "mol/L·s", "L/mol·s", "s⁻¹", "L²/mol²·s", 3, 1),
                            ("The activation energy is the", "Energy released in reaction", "Minimum energy for reaction to occur", "Average kinetic energy", "Enthalpy change", 2, 1),
                            ("A catalyst increases reaction rate by", "Increasing temperature", "Lowering activation energy", "Increasing concentration", "Changing equilibrium constant", 2, 1),
                        ],
                    },
                    {
                        "title": "Collision Theory and Arrhenius Equation",
                        "description": "Temperature dependence, frequency factor, threshold energy",
                        "time_duration": 15,
                        "questions": [
                            ("Arrhenius equation is k = Ae^(-Ea/RT). Here A is called", "Rate constant", "Frequency factor", "Activation energy", "Gas constant", 2, 1),
                            ("Increasing temperature increases rate mainly because", "Collisions increase only", "Fraction of effective collisions increases", "Activation energy decreases permanently", "Concentration increases", 2, 1),
                            ("The slope of ln(k) vs 1/T graph gives", "-Ea/R", "Ea/R", "-Ea", "Ea", 1, 1),
                            ("Zero-order reactions have rate that is", "Proportional to concentration", "Inversely proportional", "Independent of concentration", "Proportional to square of concentration", 3, 1),
                            ("The molecularity of a reaction can be", "Zero", "Fractional", "Only 1, 2, or 3", "Any positive number", 3, 1),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "name": "Mathematics",
        "description": "Calculus, algebra, vectors, 3D geometry, probability & more",
        "chapters": [
            {
                "name": "Continuity and Differentiability",
                "description": "Limits, continuity, chain rule, mean value theorems",
                "quizzes": [
                    {
                        "title": "Continuity and Derivatives",
                        "description": "Conditions for continuity, derivatives of standard functions",
                        "time_duration": 20,
                        "questions": [
                            ("A function is continuous at x = a if limit = f(a) and", "Derivative exists", "Limit exists", "Both sides of limit are equal", "All three conditions hold", 4, 1),
                            ("Derivative of sin(x) with respect to x is", "cos(x)", "-cos(x)", "sin(x)", "-sin(x)", 1, 1),
                            ("Derivative of e^(ax) is", "e^(ax)", "a·e^(ax)", "ax·e^(ax-1)", "e^(ax)/a", 2, 1),
                            ("The chain rule is used when differentiating", "Sum of functions", "Product of functions", "Composite functions", "Quotient of functions", 3, 1),
                            ("Rolle's theorem requires the function to be continuous on [a,b], differentiable on (a,b), and", "f(a) < f(b)", "f(a) = f(b)", "f(a) > f(b)", "f'(a) = 0", 2, 1),
                        ],
                    },
                    {
                        "title": "Application of Derivatives",
                        "description": "Maxima, minima, increasing/decreasing functions, tangents",
                        "time_duration": 20,
                        "questions": [
                            ("A function is increasing on an interval if its derivative is", "Negative", "Zero", "Positive", "Undefined", 3, 1),
                            ("For a local maximum at x = c, the second derivative is", "Positive", "Negative", "Zero", "Undefined", 2, 1),
                            ("The equation of tangent to y = f(x) at point (x₁,y₁) uses the slope", "f(x₁)", "1/f'(x₁)", "f'(x₁)", "-1/f'(x₁)", 3, 1),
                            ("Rate of change of area of a circle with radius is", "π", "2πr", "πr²", "2π", 2, 1),
                            ("The point where curve changes concavity is called", "Maximum", "Minimum", "Inflection point", "Saddle point", 3, 1),
                        ],
                    },
                ],
            },
            {
                "name": "Integrals",
                "description": "Indefinite and definite integrals, fundamental theorem of calculus",
                "quizzes": [
                    {
                        "title": "Integration Techniques",
                        "description": "Substitution, integration by parts, partial fractions",
                        "time_duration": 20,
                        "questions": [
                            ("∫sin(x)dx equals", "-cos(x) + C", "cos(x) + C", "sin(x) + C", "-sin(x) + C", 1, 1),
                            ("Integration by parts uses the formula ∫u dv =", "uv - ∫v du", "uv + ∫v du", "∫u v dx", "u/v + C", 1, 1),
                            ("∫eˣ dx equals", "eˣ/x + C", "xeˣ + C", "eˣ + C", "e^(x+1) + C", 3, 1),
                            ("∫1/x dx equals", "x + C", "ln|x| + C", "1/x² + C", "x² + C", 2, 1),
                            ("The integral ∫₀^π sin(x)dx equals", "0", "1", "2", "π", 3, 1),
                        ],
                    },
                    {
                        "title": "Definite Integrals and Area",
                        "description": "Properties of definite integrals, area between curves",
                        "time_duration": 20,
                        "questions": [
                            ("The area enclosed between y=x² and y=x is", "1/2", "1/6", "1/3", "1/4", 2, 1),
                            ("∫₋ₐ^ₐ f(x)dx = 0 when f(x) is", "Even function", "Odd function", "Constant", "Monotone", 2, 1),
                            ("Fundamental Theorem of Calculus states d/dx ∫ₐˣ f(t)dt =", "f(a)", "f(x)", "F(x) - F(a)", "0", 2, 1),
                            ("∫₀^1 x dx equals", "1", "1/2", "2", "0", 2, 1),
                            ("Area of circle of radius r using integration is", "2πr", "πr", "πr²", "2πr²", 3, 1),
                        ],
                    },
                ],
            },
            {
                "name": "Probability",
                "description": "Conditional probability, Bayes' theorem, random variables",
                "quizzes": [
                    {
                        "title": "Conditional Probability and Bayes' Theorem",
                        "description": "P(A|B), multiplication rule, total probability",
                        "time_duration": 15,
                        "questions": [
                            ("P(A|B) is defined as", "P(A∩B)/P(A)", "P(A∩B)/P(B)", "P(A)×P(B)", "P(A∪B)/P(B)", 2, 1),
                            ("Two events are independent if P(A∩B) =", "P(A) + P(B)", "P(A) × P(B)", "P(A) - P(B)", "P(A|B)", 2, 1),
                            ("Bayes' theorem is used to find", "Prior probability", "Posterior probability", "Marginal probability", "Joint probability", 2, 1),
                            ("If P(A) = 0.4 and P(B) = 0.3 and A,B independent then P(A∩B) =", "0.7", "0.1", "0.12", "0.58", 3, 1),
                            ("The sum of all probabilities in a sample space is", "0", "0.5", "1", "Depends on events", 3, 1),
                        ],
                    },
                    {
                        "title": "Random Variables and Distributions",
                        "description": "Binomial distribution, mean, variance",
                        "time_duration": 15,
                        "questions": [
                            ("Expected value E(X) of a discrete random variable is", "ΣP(X)", "ΣxP(x)", "ΣP(x)²", "Σx/n", 2, 1),
                            ("Variance is defined as E(X²) minus", "E(X)", "[E(X)]²", "E(X)/n", "E(X²)", 2, 1),
                            ("In Binomial distribution B(n,p), mean is", "np", "npq", "np²", "n/p", 1, 1),
                            ("Bernoulli trial has exactly how many outcomes?", "1", "2", "3", "Infinite", 2, 1),
                            ("For B(n,p), variance is", "np", "npq", "nq", "np²q", 2, 1),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "name": "Biology",
        "description": "Reproduction, genetics, evolution, biotechnology & ecosystem",
        "chapters": [
            {
                "name": "Principles of Inheritance and Variation",
                "description": "Mendel's laws, chromosomal theory, genetic disorders",
                "quizzes": [
                    {
                        "title": "Mendel's Laws",
                        "description": "Law of segregation, independent assortment, monohybrid cross",
                        "time_duration": 15,
                        "questions": [
                            ("Mendel's Law of Segregation states that alleles", "Blend together", "Separate during gamete formation", "Are always dominant", "Are always recessive", 2, 1),
                            ("In a monohybrid cross Aa × Aa the phenotypic ratio is", "1:1", "3:1", "1:2:1", "9:3:3:1", 2, 1),
                            ("A test cross involves crossing with a", "Homozygous dominant", "Heterozygous individual", "Homozygous recessive", "F1 hybrid", 3, 1),
                            ("Chromosomal theory of inheritance was proposed by", "Mendel", "Watson and Crick", "Sutton and Boveri", "Morgan", 3, 1),
                            ("A person with genotype AaBb can produce how many types of gametes?", "1", "2", "4", "8", 3, 1),
                        ],
                    },
                    {
                        "title": "Chromosomal Disorders and Linkage",
                        "description": "Sex-linked traits, chromosomal mutations, pedigree analysis",
                        "time_duration": 15,
                        "questions": [
                            ("Haemophilia is a", "Autosomal dominant disorder", "Autosomal recessive disorder", "X-linked recessive disorder", "Y-linked disorder", 3, 1),
                            ("Down syndrome is caused by trisomy of chromosome", "21", "18", "13", "X", 1, 1),
                            ("Sex determination in humans depends on the chromosome contributed by", "Mother", "Father", "Both equally", "Neither parent", 2, 1),
                            ("Linked genes tend to be inherited together because they are on", "Different chromosomes", "Same chromosome", "Homologous chromosomes", "Mitochondria", 2, 1),
                            ("Turner syndrome has the karyotype", "47 XXY", "47 XYY", "45 XO", "47 XXX", 3, 1),
                        ],
                    },
                ],
            },
            {
                "name": "Molecular Basis of Inheritance",
                "description": "DNA structure, replication, transcription, translation",
                "quizzes": [
                    {
                        "title": "DNA Structure and Replication",
                        "description": "Double helix, base pairing, semi-conservative replication",
                        "time_duration": 20,
                        "questions": [
                            ("DNA double helix was proposed by", "Mendel and Morgan", "Watson and Crick", "Chargaff and Franklin", "Hershey and Chase", 2, 1),
                            ("In DNA, adenine pairs with", "Cytosine", "Guanine", "Thymine", "Uracil", 3, 1),
                            ("DNA replication is called semi-conservative because", "One strand is conserved", "Half the DNA is conserved", "Each new DNA has one old and one new strand", "DNA is partially degraded", 3, 1),
                            ("The enzyme that joins Okazaki fragments is", "Helicase", "DNA polymerase", "DNA ligase", "Primase", 3, 1),
                            ("The sugar in DNA is", "Ribose", "Fructose", "Deoxyribose", "Glucose", 3, 1),
                        ],
                    },
                    {
                        "title": "Transcription, Translation and Gene Regulation",
                        "description": "mRNA, codons, ribosomes, lac operon",
                        "time_duration": 20,
                        "questions": [
                            ("The process of copying DNA into mRNA is called", "Translation", "Transcription", "Replication", "Transduction", 2, 1),
                            ("A codon consists of how many nucleotides?", "2", "3", "4", "1", 2, 1),
                            ("The start codon in eukaryotes is", "UAG", "UAA", "AUG", "UGA", 3, 1),
                            ("The lac operon is an example of", "Positive regulation only", "Negative regulation only", "Inducible operon", "Repressible operon", 3, 1),
                            ("tRNA carries amino acids to the", "Nucleus", "Ribosome", "Mitochondria", "Endoplasmic reticulum", 2, 1),
                        ],
                    },
                ],
            },
            {
                "name": "Evolution",
                "description": "Darwin's theory, natural selection, speciation, human evolution",
                "quizzes": [
                    {
                        "title": "Theories of Evolution",
                        "description": "Lamarck, Darwin, Hardy-Weinberg principle",
                        "time_duration": 15,
                        "questions": [
                            ("Darwin's theory of evolution is based on", "Use and disuse of organs", "Natural selection and survival of the fittest", "Inheritance of acquired characters", "Mutation only", 2, 1),
                            ("Hardy-Weinberg equilibrium requires", "Large population, no migration, no mutation, random mating", "Small population", "High mutation rate", "Non-random mating", 1, 1),
                            ("Analogous organs are similar in", "Origin", "Function", "Structure and origin", "Embryonic development", 2, 1),
                            ("The first life forms on Earth were", "Multicellular organisms", "Fungi", "Chemoheterotrophs", "Autotrophs", 3, 1),
                            ("Industrial melanism in peppered moths is an example of", "Genetic drift", "Natural selection", "Sexual selection", "Mutation", 2, 1),
                        ],
                    },
                    {
                        "title": "Human Evolution and Speciation",
                        "description": "Hominid evolution, allopatric and sympatric speciation",
                        "time_duration": 15,
                        "questions": [
                            ("Homo sapiens appeared approximately", "15 million years ago", "2 million years ago", "75,000 years ago", "500,000 years ago", 4, 1),
                            ("Allopatric speciation occurs due to", "Behavioural differences", "Geographical isolation", "Temporal isolation", "Genetic compatibility", 2, 1),
                            ("The closest living relative of humans is the", "Gorilla", "Orangutan", "Chimpanzee", "Gibbon", 3, 1),
                            ("Adaptive radiation is seen in", "Darwin's finches", "Homologous organs only", "Single isolated species", "Aquatic animals only", 1, 1),
                            ("The first Homo sapiens fossils were found in", "Asia", "Europe", "Africa", "Americas", 3, 1),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "name": "English",
        "description": "Flamingo, Vistas, grammar, writing skills and comprehension",
        "chapters": [
            {
                "name": "Flamingo — Prose",
                "description": "The Last Lesson, Lost Spring, Deep Water, The Rattrap and more",
                "quizzes": [
                    {
                        "title": "The Last Lesson & Lost Spring",
                        "description": "Comprehension and literary analysis of two short stories",
                        "time_duration": 15,
                        "questions": [
                            ("In 'The Last Lesson', Franz was afraid because he had not learnt", "History", "French grammar", "Mathematics", "German", 2, 1),
                            ("'The Last Lesson' is written by", "Pearl S. Buck", "Alphonse Daudet", "Kamala Das", "William Saroyan", 2, 1),
                            ("In 'Lost Spring', Saheb means", "Lord of the Universe", "Child of the streets", "Master of work", "Free bird", 1, 1),
                            ("Saheb and his family migrated from", "Bangladesh", "Pakistan", "Nepal", "Sri Lanka", 1, 1),
                            ("The ironical title 'Lost Spring' refers to", "Lost monsoon", "Lost childhood — spring of life", "Loss of a season", "Pollution of rivers", 2, 1),
                        ],
                    },
                    {
                        "title": "Deep Water & The Rattrap",
                        "description": "Fear, redemption and human nature in two contrasting stories",
                        "time_duration": 15,
                        "questions": [
                            ("In 'Deep Water', W.O. Douglas was afraid of", "Heights", "Water", "Darkness", "Fire", 2, 1),
                            ("Douglas overcame his fear by", "Avoiding water", "Taking swimming lessons", "Meditation", "Reading books", 2, 1),
                            ("The rattrap seller in 'The Rattrap' is a", "Wealthy businessman", "Poor vagabond", "Soldier", "Farmer", 2, 1),
                            ("Edla Willmansson's gesture towards the rattrap seller shows", "Cunning", "Kindness and dignity", "Fear", "Business acumen", 2, 1),
                            ("The central theme of 'The Rattrap' is", "Capitalism", "Human redemption through love and compassion", "Adventure", "War", 2, 1),
                        ],
                    },
                ],
            },
            {
                "name": "Flamingo — Poetry",
                "description": "My Mother at Sixty-Six, An Elementary School Classroom and more",
                "quizzes": [
                    {
                        "title": "Poetry Comprehension",
                        "description": "Themes and literary devices in Class 12 poems",
                        "time_duration": 15,
                        "questions": [
                            ("'My Mother at Sixty-Six' is written by", "Kamala Das", "Adrienne Rich", "Rabindranath Tagore", "Pablo Neruda", 1, 1),
                            ("In 'My Mother at Sixty-Six' the poet compares her mother's face to a", "Pale moon", "Corpse that's late", "White flower", "Snow-capped mountain", 2, 1),
                            ("'Keeping Quiet' is originally written in", "English", "Spanish", "Portuguese", "Hindi", 3, 1),
                            ("The poem 'A Thing of Beauty' is by", "John Keats", "P.B. Shelley", "William Blake", "William Wordsworth", 1, 1),
                            ("'An Elementary School Classroom in a Slum' is written by", "Stephen Spender", "W.H. Auden", "T.S. Eliot", "John Donne", 1, 1),
                        ],
                    },
                    {
                        "title": "Literary Devices and Themes",
                        "description": "Identify figures of speech and central themes in poems",
                        "time_duration": 10,
                        "questions": [
                            ("Personification means attributing human qualities to", "Animals only", "Abstract ideas or non-human things", "Natural phenomena only", "Animate objects", 2, 1),
                            ("A metaphor is a direct comparison", "Using 'like' or 'as'", "Without using 'like' or 'as'", "With a full simile", "Using imagery only", 2, 1),
                            ("Alliteration is repetition of", "Vowel sounds", "Initial consonant sounds in nearby words", "End sounds", "Middle sounds", 2, 1),
                            ("The central theme of 'Keeping Quiet' is", "War glorification", "Silence and self-reflection for peace", "Nature conservation", "Political freedom", 2, 1),
                            ("Enjambment means", "End-stopped lines", "Continuation of a sentence beyond the end of a line", "Rhyming couplets", "Short, punchy lines", 2, 1),
                        ],
                    },
                ],
            },
            {
                "name": "Writing Skills and Grammar",
                "description": "Notice, letter, report writing, articles and grammar exercises",
                "quizzes": [
                    {
                        "title": "Formal Writing — Notices and Letters",
                        "description": "Format, tone, and content of formal communication",
                        "time_duration": 15,
                        "questions": [
                            ("A notice should always be", "Long and detailed", "Brief, clear and to the point", "Written in first person", "Informal in tone", 2, 1),
                            ("An official letter ends with", "Yours lovingly", "Yours sincerely or faithfully", "Best wishes", "Regards only", 2, 1),
                            ("A job application letter must include", "Personal gossip", "Educational qualifications and relevant experience", "Salary demands upfront", "Casual language", 2, 1),
                            ("The subject line in a formal letter", "Is optional", "Comes after the salutation", "Briefly states the purpose of the letter", "Is written in lowercase", 3, 1),
                            ("In a formal letter 'Yours faithfully' is used when the salutation is", "Dear [Name]", "Dear Sir/Madam", "Hi", "To whom it may concern only", 2, 1),
                        ],
                    },
                    {
                        "title": "Grammar — Tenses and Voice",
                        "description": "Active/passive voice, tenses, reported speech",
                        "time_duration": 15,
                        "questions": [
                            ("In passive voice 'She sings a song' becomes", "A song is sang by her", "A song is being sung by her", "A song is sung by her", "A song was sung by her", 3, 1),
                            ("'He said, \"I am happy\"' in indirect speech becomes", "He said that I was happy", "He said that he was happy", "He told that he is happy", "He said he is happy", 2, 1),
                            ("The present perfect tense is used for", "Habitual actions", "Actions just completed having present relevance", "Future plans", "Ongoing past actions", 2, 1),
                            ("Choose the correct sentence", "She don't know", "She doesn't knows", "She doesn't know", "She not know", 3, 1),
                            ("'Either … or' is used with a", "Plural verb always", "Singular verb when both subjects are singular", "Verb matching the nearest subject", "Both B and C", 4, 1),
                        ],
                    },
                ],
            },
        ],
    },
]

USERS = [
    {"username": "arjun.sharma@student.com",  "full_name": "Arjun Sharma",   "qualification": "Class 12", "dob": "2007-03-15"},
    {"username": "priya.patel@student.com",   "full_name": "Priya Patel",    "qualification": "Class 12", "dob": "2007-06-22"},
    {"username": "rahul.verma@student.com",   "full_name": "Rahul Verma",    "qualification": "Class 12", "dob": "2007-01-08"},
    {"username": "sneha.gupta@student.com",   "full_name": "Sneha Gupta",    "qualification": "Class 12", "dob": "2007-09-30"},
    {"username": "karan.singh@student.com",   "full_name": "Karan Singh",    "qualification": "Class 12", "dob": "2007-11-14"},
    {"username": "ananya.rao@student.com",    "full_name": "Ananya Rao",     "qualification": "Class 12", "dob": "2007-04-05"},
    {"username": "dev.kumar@student.com",     "full_name": "Dev Kumar",      "qualification": "Class 12", "dob": "2007-07-18"},
    {"username": "meera.iyer@student.com",    "full_name": "Meera Iyer",     "qualification": "Class 12", "dob": "2007-02-27"},
    {"username": "rohit.mishra@student.com",  "full_name": "Rohit Mishra",   "qualification": "Class 12", "dob": "2007-08-11"},
    {"username": "nisha.joshi@student.com",   "full_name": "Nisha Joshi",    "qualification": "Class 12", "dob": "2007-12-03"},
]

# ─────────────────────────────────────────────────────────────
# Seeding logic
# ─────────────────────────────────────────────────────────────

def seed():
    with app.app_context():
        print("Starting seed…")

        # ── Users ──────────────────────────────────────────────
        created_users = []
        for u in USERS:
            existing = User.query.filter_by(username=u["username"]).first()
            if existing:
                created_users.append(existing)
                continue
            user = User(
                username=u["username"],
                email=u["username"],
                full_name=u["full_name"],
                qualification=u["qualification"],
                dob=datetime.strptime(u["dob"], "%Y-%m-%d").date(),
                role="user",
            )
            user.set_password("student123")
            db.session.add(user)
            db.session.flush()
            created_users.append(user)
            print(f"  Created user: {u['full_name']}")
        db.session.commit()

        # ── Subjects / Chapters / Quizzes / Questions ──────────
        all_quizzes = []
        for s_data in SUBJECTS:
            subject = Subject.query.filter_by(name=s_data["name"]).first()
            if not subject:
                subject = Subject(name=s_data["name"], description=s_data["description"])
                db.session.add(subject)
                db.session.flush()
                print(f"  Created subject: {s_data['name']}")

            for c_data in s_data["chapters"]:
                chapter = Chapter.query.filter_by(name=c_data["name"], subject_id=subject.id).first()
                if not chapter:
                    chapter = Chapter(name=c_data["name"], description=c_data["description"], subject_id=subject.id)
                    db.session.add(chapter)
                    db.session.flush()

                for q_data in c_data["quizzes"]:
                    quiz = Quiz.query.filter_by(title=q_data["title"], chapter_id=chapter.id).first()
                    if not quiz:
                        quiz = Quiz(
                            title=q_data["title"],
                            description=q_data["description"],
                            chapter_id=chapter.id,
                            date_of_quiz=datetime.utcnow() - timedelta(days=random.randint(1, 60)),
                            time_duration=q_data["time_duration"],
                            total_marks=0,
                        )
                        db.session.add(quiz)
                        db.session.flush()

                        total = 0
                        for stmt, o1, o2, o3, o4, correct, marks in q_data["questions"]:
                            q = Question(
                                quiz_id=quiz.id,
                                question_statement=stmt,
                                option1=o1, option2=o2, option3=o3, option4=o4,
                                correct_option=correct,
                                marks=marks,
                            )
                            db.session.add(q)
                            total += marks
                        quiz.total_marks = total
                        db.session.flush()
                        print(f"    Quiz: {q_data['title']}")

                    all_quizzes.append(quiz)

        db.session.commit()

        # ── Placeholder attempts ───────────────────────────────
        # Each user attempts 60-80% of quizzes with varied performance
        print("\nCreating quiz attempts…")
        for user in created_users:
            sample_size = int(len(all_quizzes) * random.uniform(0.55, 0.85))
            selected = random.sample(all_quizzes, sample_size)

            for quiz in selected:
                existing = Score.query.filter_by(user_id=user.id, quiz_id=quiz.id).first()
                if existing:
                    continue

                # Simulate answer selections (mostly correct)
                questions = Question.query.filter_by(quiz_id=quiz.id).all()
                correct_count = 0
                answers = {}
                for q in questions:
                    # 55-90% chance of getting each question right based on user
                    user_idx = created_users.index(user)
                    base_prob = 0.55 + (user_idx / len(created_users)) * 0.35
                    if random.random() < base_prob:
                        answers[str(q.id)] = q.correct_option
                        correct_count += q.marks
                    else:
                        wrong = random.choice([x for x in [1, 2, 3, 4] if x != q.correct_option])
                        answers[str(q.id)] = wrong

                # Random attempt time in the past 60 days
                attempt_time = datetime.utcnow() - timedelta(
                    days=random.randint(1, 60),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )

                score = Score(
                    quiz_id=quiz.id,
                    user_id=user.id,
                    total_scored=correct_count,
                    total_marks=quiz.total_marks,
                    time_taken=random.randint(5, quiz.time_duration),
                    timestamp_of_attempt=attempt_time,
                    answers=answers,
                )
                db.session.add(score)

        db.session.commit()
        print("\nSeed complete!")
        print(f"  Subjects : {len(SUBJECTS)}")
        print(f"  Quizzes  : {len(all_quizzes)}")
        print(f"  Users    : {len(created_users)}")
        print(f"\nStudent login password: student123")
        print(f"Admin login           : admin / admin123")

if __name__ == "__main__":
    seed()
