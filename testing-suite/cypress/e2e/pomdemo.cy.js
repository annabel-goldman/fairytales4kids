import { HomePage } from "./pages/homePage.cy"

const homePage = new HomePage

describe('Basic navigation test', () => {
    beforeEach(function(){
        cy.visit('/')
    })

    it('should navigate to stories page', () => {
        homePage.clickEnter()
        cy.url().should('include', 'stories.html')
    })
})
