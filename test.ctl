(set! geometry-lattice (make lattice (size 5 5 no-size)))
(set! geometry (list (make cylinder 
                       (center 0 0 0) (radius 0.2) (height infinity)
                       (material (make dielectric (epsilon 12))))))

(set! geometry (geometric-objects-lattice-duplicates geometry))

(set! geometry (append geometry
					(list (make cylinder (center 0 0 0)
					(radius 0.2) (height infinity)
					(material air)))))

(set! resolution 16)

(set! k-points (list (vector3 0.5 0.5 0)))

(set! num-bands 100)

(run-tm)
(output-efield-z 25)