import { HomePage } from "./pages/homePage.cy"

const homePage = new HomePage

describe('All story tests', () => {
    beforeEach(function(){
        cy.visit('https://fairytales4kids.com')
    })

    it('Little Red Riding Hood Test', () => {
        homePage.clickEnter()
        cy.get('[href="stories/little-red-riding-hood.html"]').click()
        cy.get('.back-button').click()
    })

})
